# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker:
    def __init__(self, maxDisappeared=50):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappeared = maxDisappeared

    def register(self, centroid):
        # when registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.nextObjectID] = centroid
        # FIXME don't need this? clears the next centroid (USED FOR NOW FOR ITR)
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]

    def _needs_updates(self, rects) -> bool:
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them
            # as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                # if we have reached a maximum number of consecutive
                # frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            # return early as there are no centroids or tracking info
            # to update
            # return self.objects
            return False
        return True

    def _creating_input_centroids(self, rects):
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for i, (startX, startY, endX, endY) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])
        return inputCentroids

    def _compute_distance_from_tracked_centroid(self, inputCentroids):
        objectIDs = list(self.objects.keys())
        objectCentroids = list(self.objects.values())

        dist_from_tracked = dist.cdist(np.array(objectCentroids), inputCentroids)
        # in order to perform this matching we must
        # (1) find the smallest value in each row and then
        # (2) sort the row indexes based on their minimum values so that the row # with the smallest value is at the *front* of the index list
        try:
            rows = dist_from_tracked.min(axis=1).argsort()
        except ValueError:
            print(
                f"VALUEERROR Rows was empty D = {dist_from_tracked}, {inputCentroids}"
            )
            rows = np.array([])
        # next, we perform a similar process on the columns by
        # finding the smallest value in each column and then
        # sorting using the previously computed row index list
        try:
            cols = dist_from_tracked.argmin(axis=1)[rows]
        except ValueError:
            print(
                f"VALUEERROR Cols was empty D = {dist_from_tracked}, {inputCentroids}"
            )
            cols = np.array([])
        usedRows = set()
        usedCols = set()
        for row, col in zip(rows, cols):
            # ignore previously examined row,col
            if row in usedRows or col in usedCols:
                continue
            # this object disappeared
            objectID = objectIDs[row]
            self.objects[objectID] = inputCentroids[col]
            self.disappeared[objectID] = 0
            # indicate that we have examined each of the row and
            # column indexes, respectively
            usedRows.add(row)
            usedCols.add(col)
        return dist_from_tracked, usedRows, usedCols

    def _remove_unused_objects(
        self, centroid_distances, inputCentroids, usedRows, usedCols
    ):
        D = centroid_distances
        objectIDs = list(self.objects.keys())
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

    def update(self, rects):
        # Step 1: Check if you need updates (do we have any mines?)
        print(f"\nStarting 'update' Step 1: Checking if we found any objects")
        if not self._needs_updates:
            return
        print(f"Starting 'update' Step 2: Registering new IDs")
        # Step 2: Create input centroids and register if frame is blank
        inputCentroids = self._creating_input_centroids(rects)

        # Setp 3: Needs to track with existing centrois
        if len(self.objects) != 0:
            print(f"Starting 'update' Step 3: Found multiple objects in the same frame")
            print(
                f"Starting 'update' Step 3.1: Checking how close object is to previous objects"
            )
            # 3.1 Calculate how close current centroid is to the previously found centroids
            D, usedRows, usedCols = self._compute_distance_from_tracked_centroid(
                inputCentroids
            )
            print(f"Starting 'update' Step 3.2: Unregistering old objects")
            # 3.2 Unregister extras that have disappeared
            self._remove_unused_objects(D, inputCentroids, usedRows, usedCols)
        return self.objects
