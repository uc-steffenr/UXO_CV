# import the necessary packages
from typing import List
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
from uuid import uuid4

import coloredlogs, logging

logger = logging.getLogger(__name__)
msg_format = "%(asctime)s %(name)s\t%(levelname)s %(message)s"
coloredlogs.install(level="DEBUG", fmt=msg_format, datefmt="%H:%M:%S", logger=logger)


class OpticalFlow:
    pass


class CentroidTracker:
    def __init__(self, frames_needed: int = 3):
        # how many frames in a row to confirm a track as real
        self.frames_needed = frames_needed

        self.infant_tracks = (
            OrderedDict()
        )  # any identified obj yet to be confirmed, past and present
        self.infant_track_occurance = OrderedDict()  # how many times an obj was seen
        self.all_known_objects = OrderedDict()  # all confirmed objs, past and present

        # objs from last frame, confirmed and unconfirmed (ID, centroid)
        self.previous_objects = OrderedDict()
        self.current_objects = OrderedDict()  # all objs in current frame
        self.disappeared_objects: List[str] = []  # confirmed objs not in current frame

        self.nextObjectID = 0  # objID to use, if int

    def register_unconfirmed(self, centroid, use_guid: bool = False):
        if use_guid:
            this_id = uuid4()
            self.infant_tracks[this_id] = centroid
        else:
            self.infant_tracks[self.nextObjectID] = centroid
            self.infant_track_occurance[self.nextObjectID] = 1
            this_id = self.nextObjectID
            self.nextObjectID += 1
        logger.debug(f"Register uncomfirmed object {this_id}, {centroid}")
        self.current_objects[this_id] = centroid
        return this_id, centroid

    def deregister(self, objectID):
        del self.previous_objects[objectID]
        del self.disappeared[objectID]
        # del self.infant_tracks[objectID]
        # del self.all_known_objects[objectID]

    def _needs_updates(self, rects) -> bool:
        if len(rects) == 0:
            for objectID in self.previous_objects:
                self.disappeared_objects.append(objectID)
            return False
        return True

    def _creating_input_centroids(self, rects):
        inputCentroids = []
        for startX, startY, endX, endY in rects:
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids.append((cX, cY))

        if len(self.all_known_objects) == 0 and len(self.previous_objects) == 0:
            for i in range(0, len(inputCentroids)):
                logger.debug(f"Case 1: Never seen an obj, found an obj")
                self.register_unconfirmed(inputCentroids[i])
        return inputCentroids

    def _compute_distance_from_tracked_centroid(self, inputCentroids, tol_px=20):
        previousobjectIDs = list(self.previous_objects.keys())
        previousCentroids = list(self.previous_objects.values())
        # Case 2A: have seen some objects before but there weren't any in previous frame
        if len(self.previous_objects) == 0 and len(self.all_known_objects) != 0:
            logger.debug(f"Case 2A: Seen new obj, have to check the known objs list")
            for cx, cy in inputCentroids:
                geoloc = False
                # TODO do geolocation comparison here
                logger.warning(f"TODO geoloc here")
                if not geoloc:
                    logger.debug(f"Registering new track-- not previously located")
                    self.register_unconfirmed((cx, cy))
        # Case 2B: have seen some objects before, we saw some previously, and now we need to match
        else:
            logger.debug(
                f"Case 2B: Seen new obj and previously saw objs. Trying to link together"
            )
            for found_centroid in inputCentroids:
                ref = np.array(found_centroid)
                # Euclidean distance CHECKME-- is this faster?
                # distances = dist.cdist(np.array(previousCentroids), [ref])
                # Frobenius norm
                distances = np.linalg.norm(previousCentroids - ref, axis=1)
                min_index = np.argmin(distances)
                closest_dist = distances[min_index]
                logger.info(
                    f"Centroid ({found_centroid}) is closest to {previousCentroids[min_index]} with a distance of {round(closest_dist,3)}"
                )
                if closest_dist < tol_px:
                    matching_id = previousobjectIDs[
                        previousCentroids.index(previousCentroids[min_index])
                    ]
                    logger.info(
                        f"Distance is within tolerance of {tol_px} pixels, updating infant occurances of ID {matching_id}"
                    )
                    self.infant_track_occurance[matching_id] += 1
                    self.current_objects[matching_id] = found_centroid  # FIXME
                else:
                    logger.warning(f"Case 4: FIXME")
                    self.disappeared_objects.append(previousobjectIDs)
                    self.register_unconfirmed(found_centroid)

    def _remove_unused_objects(
        self, centroid_distances, inputCentroids, usedRows, usedCols
    ):
        D = centroid_distances
        objectIDs = list(self.all_known_objects.keys())
        # compute both the row and column index we have NOT yet
        # examined
        unusedRows = set(range(0, D.shape[0])).difference(usedRows)
        unusedCols = set(range(0, D.shape[1])).difference(usedCols)
        # in the event that the number of object centroids is
        # equal or greater than the number of input centroids
        # we need to check and see if some of these objects have
        # potentially disappeared
        if D.shape[0] >= D.shape[1]:
            # loop over the unused row indexes
            for row in unusedRows:
                # grab the object ID for the corresponding row
                # index and increment the disappeared counter
                objectID = objectIDs[row]
                self.disappeared[objectID] += 1
                # get rid of the disappeared in objects
                # self.objects.pop(objectID, None)
                # reset to disappeared count
                # self.objects[objectID] = list(self.disappeared[objectID]) #doesn't work
                # check to see if the number of consecutive
                # frames the object has been marked "disappeared"
                # for warrants deregistering the object
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
        # otherwise, if the number of input centroids is greater
        # than the number of existing object centroids we need to
        # register each new input centroid as a trackable object
        else:
            for col in unusedCols:
                self.register(inputCentroids[col])

    def _confirm_objects(self):
        for objID, times_seen in self.infant_track_occurance.items():
            if times_seen >= 3 and objID not in self.all_known_objects.keys():
                if objID not in self.all_known_objects.keys():
                    logger.info(f"Confirming new object")
                    obj_centroid = self.infant_tracks[objID]
                    self.all_known_objects[objID] = obj_centroid
                    del self.infant_tracks[objID]

    def _reset(self, inputCentroids):
        self.previous_objects.clear()
        for objID, centroid in self.current_objects.items():
            if centroid in inputCentroids:
                logger.debug(
                    f"Adding {objID},{centroid} to previous_objects from current_objects"
                )
                self.previous_objects[objID] = centroid

        # if len(self.previous_objects.keys()) != len(inputCentroids):
        #     logger.warning(
        #         f"Previous Objects ({len(self.previous_objects.keys())}) and Input Centroids ({len(inputCentroids)}) do not match!"
        #     )
        #     for objID, centroid in self.all_known_objects.items():
        #         if centroid in inputCentroids:
        #             logger.debug(
        #                 f"Adding {objID},{centroid} to previous_objects from all_known_objects"
        #             )
        #             self.previous_objects[objID] = centroid
        self.current_objects.clear()
        if len(self.previous_objects.keys()) != len(inputCentroids):
            logger.warning(
                f"FINAL Previous Objects ({len(self.previous_objects.keys())}) and Input Centroids ({len(inputCentroids)}) do not match!"
            )

    def update(self, rects):
        # Step 1: Check if you need updates (do we have any objs?)
        logger.debug(f"\n")
        logger.debug(f"Starting 'update' Step 1: Checking if we found any objects")
        if not self._needs_updates(rects):
            logger.info(f"Didn't find any objects")
            return
        logger.info(f"Found some objects, moving on to Step 2")
        logger.debug(f"\n")
        logger.debug(
            f"Starting 'update' Step 2: Create input centroids and register infant tracks if possible "
        )
        # Step 2: Create input centroids and register if frame is blank
        inputCentroids = self._creating_input_centroids(rects)

        # Setp 3: Needs to track with existing centroids
        if len(list(self.previous_objects.keys())) != 0:
            logger.debug(f"\n")
            logger.debug(f"Starting 'update' Step 3: Track with existing centroids")
            self._compute_distance_from_tracked_centroid(inputCentroids)
        logger.debug(f"Starting 'update' Step 4: Resetting Variables")
        self._confirm_objects()
        self._reset(inputCentroids)
        return self.previous_objects
