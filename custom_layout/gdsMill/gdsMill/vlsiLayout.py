from gdsPrimitives import *
from datetime import *
import mpmath

class VlsiLayout:
    """Class represent a hierarchical layout"""
    def __init__(self, name=None, units=(0.001,1e-9), libraryName = "DEFAULT.DB", gdsVersion=5):
        #keep a list of all the structures in this layout
        self.units = units
        modDate = datetime.now()
        self.structures=dict()
        self.layerNumbersInUse = []
        if name:
            self.rootStructureName=name
            #create the ROOT structure
            self.structures[self.rootStructureName] = GdsStructure()
            self.structures[self.rootStructureName].name = name
            self.structures[self.rootStructureName].createDate = (modDate.year,
                                                                  modDate.month,
                                                                  modDate.day,
                                                                  modDate.hour,
                                                                  modDate.minute,
                                                                  modDate.second)
            self.structures[self.rootStructureName].modDate = (modDate.year,
                                                               modDate.month,
                                                               modDate.day,
                                                               modDate.hour,
                                                               modDate.minute,
                                                               modDate.second)
        
        self.info = dict()  #information gathered from the GDSII header
        self.info['units']=units
        self.info['dates']=(modDate.year,
                            modDate.month,
                            modDate.day,
                            modDate.hour,
                            modDate.minute,
                            modDate.second,
                            modDate.year,
                            modDate.month,
                            modDate.day,
                            modDate.hour,
                            modDate.minute,
                            modDate.second)
        self.info['libraryName']=libraryName
        self.info['gdsVersion']=gdsVersion
        
        self.xyTree = [] #This will contain a list of all structure names
                        #expanded to include srefs / arefs separately.
                        #each structure will have an X,Y,offset, and rotate associated
                        #with it.  Populate via traverseTheHierarchy method.
        
        #temp variables used in delegate functions
        self.tempCoordinates=None
        self.tempPassFail = True
    
    def rotatedCoordinates(self,coordinatesToRotate,rotateAngle):
        #helper method to rotate a list of coordinates
        angle=math.radians(float(0))
        if(rotateAngle):
            angle = math.radians(float(repr(rotateAngle)))        
        coordinatesRotate = []    #this will hold the rotated values        
        for coordinate in coordinatesToRotate:
            newX = coordinate[0]*math.cos(angle) - coordinate[1]*math.sin(angle)
            newY = coordinate[0]*math.sin(angle) + coordinate[1]*math.cos(angle)
            coordinatesRotate += [(newX,newY)]
        return coordinatesRotate
    
    def rename(self,newName):
        #make sure the newName is a multiple of 2 characters
        if(len(newName)%2 == 1):
            #pad with a zero
            newName = newName + '\x00'
        #take the root structure and copy it to a new structure with the new name
        self.structures[newName] = self.structures[self.rootStructureName]
        self.structures[newName].name = newName
        #and delete the old root
        del self.structures[self.rootStructureName]
        self.rootStructureName = newName
        #repopulate the 2d map so drawing occurs correctly
        del self.xyTree[:]
        self.populateCoordinateMap()
                        
    def deduceHierarchy(self):
        #first, find the root of the tree.
        #go through and get the name of every structure.
        #then, go through and find which structure is not
        #contained by any other structure. this is the root.
        structureNames=[]
        for name in self.structures:
            structureNames+=[name]
            
        for name in self.structures:
            if(len(self.structures[name].srefs)>0): #does this structure reference any others?
                for sref in self.structures[name].srefs: #go through each reference
                    if sref.sName in structureNames: #and compare to our list
                        structureNames.remove(sref.sName)
        
        self.rootStructureName = structureNames[0]

    def traverseTheHierarchy(self, startingStructureName=None, delegateFunction = None, transformPath = [], rotateAngle = 0, transFlags = (0,0,0), coordinates = (0,0)):
        #since this is a recursive function, must deal with the default
        #parameters explicitly        
        if startingStructureName == None:
            startingStructureName = self.rootStructureName            
        
        #set up the rotation matrix        
        if(rotateAngle == None or rotateAngle == ""):
            rotateAngle = 0
        else:
            rotateAngle = math.radians(float(rotateAngle))
        mRotate = mpmath.matrix([[math.cos(rotateAngle),-math.sin(rotateAngle),0.0],[math.sin(rotateAngle),math.cos(rotateAngle),0.0],[0.0,0.0,1.0],])
        #set up the translation matrix
        translateX = float(coordinates[0])
        translateY = float(coordinates[1])
        mTranslate = mpmath.matrix([[1.0,0.0,translateX],[0.0,1.0,translateY],[0.0,0.0,1.0]])
        #set up the scale matrix (handles mirror X)
        scaleY = 1.0
        if(transFlags[0]):
            scaleX = -1.0
        else:
            scaleX = 1.0
        mScale = mpmath.matrix([[scaleX,0.0,0.0],[0.0,scaleY,0.0],[0.0,0.0,1.0]])
        
        #we need to keep track of all transforms in the hierarchy
        #when we add an element to the xy tree, we apply all transforms from the bottom up
        transformPath += [(mRotate,mScale,mTranslate)]
        if delegateFunction != None:
            delegateFunction(startingStructureName, transformPath)
        #starting with a particular structure, we will recursively traverse the tree
        #********might have to set the recursion level deeper for big layouts!
        if(len(self.structures[startingStructureName].srefs)>0): #does this structure reference any others?
            #if so, go through each and call this function again
            #if not, return back to the caller (caller can be this function)            
            for sref in self.structures[startingStructureName].srefs:
                #here, we are going to modify the sref coordinates based on the parent objects rotation                
                self.traverseTheHierarchy(startingStructureName = sref.sName,                                    
                                          delegateFunction = delegateFunction,
                                          transformPath = transformPath,
                                          rotateAngle = sref.rotateAngle,
                                          transFlags = sref.transFlags,
                                          coordinates = sref.coordinates)
            #MUST HANDLE AREFs HERE AS WELL
        #when we return, drop the last transform from the transformPath
        del transformPath[-1]
        return
    
    def initialize(self):
        self.deduceHierarchy()
        #self.traverseTheHierarchy()
        self.populateCoordinateMap()    
    
    def populateCoordinateMap(self):
        def addToXyTree(startingStructureName = None,transformPath = None):            
            uVector = mpmath.matrix([1.0,0.0,0.0])  #start with normal basis vectors
            vVector = mpmath.matrix([0.0,1.0,0.0])
            origin = mpmath.matrix([0.0,0.0,1.0]) #and an origin (Z component is 1.0 to indicate position instead of vector)
            #make a copy of all the transforms and reverse it            
            reverseTransformPath = transformPath[:]
            if len(reverseTransformPath) > 1:
                reverseTransformPath.reverse()               
            #now go through each transform and apply them to our basis and origin in succession
            for transform in reverseTransformPath:
                origin = transform[0] * origin  #rotate
                uVector = transform[0] * uVector  #rotate
                vVector = transform[0] * vVector  #rotate
                origin = transform[1] * origin  #scale
                uVector = transform[1] * uVector  #rotate
                vVector = transform[1] * vVector  #rotate
                origin = transform[2] * origin  #translate
                #we don't need to do a translation on the basis vectors            
            self.xyTree+=[(startingStructureName,origin,uVector,vVector)]  #populate the xyTree with each
                                                                            #structureName and coordinate space
        self.traverseTheHierarchy(delegateFunction = addToXyTree)
        
    def microns(self,userUnits):
        """Utility function to convert user units to microns"""
        userUnit = self.units[1]/self.units[0]
        userUnitsPerMicron = userUnit / 1e-6
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        return userUnits / layoutUnitsPerMicron
        
    def userUnits(self,microns):
        """Utility function to convert microns to user units"""
        userUnit = self.units[1]/self.units[0]
        userUnitsPerMicron = userUnit / 1e-6
        layoutUnitsPerMicron = userUnitsPerMicron / self.units[0]
        return round(microns*layoutUnitsPerMicron)
    
    def addInstance(self,layoutToAdd,offsetInMicrons=(0,0),mirror=None,rotate=None,updateInternalMap=False):
        """
        Method to insert one layout into another at a particular offset.
        """
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        #first, we need to combine the structure dictionaries from both layouts
        for structure in layoutToAdd.structures:
            if structure not in self.structures:
                self.structures[structure]=layoutToAdd.structures[structure]
        #also combine the "layers in use" list
        for layerNumber in layoutToAdd.layerNumbersInUse:
            if layerNumber not in self.layerNumbersInUse:
                self.layerNumbersInUse += [layerNumber]
        #add a reference to the new layout structure in this layout's root
        layoutToAddSref = GdsSref()
        layoutToAddSref.sName = layoutToAdd.rootStructureName
        layoutToAddSref.coordinates = offsetInLayoutUnits
        if mirror or rotate:
            layoutToAddSref.transFlags = (False,False,False)
            if mirror == "x":
                layoutToAddSref.transFlags = (True,layoutToAddSref.transFlags[1],layoutToAddSref.transFlags[2])
            if mirror == "y":
                #mirror y = rotate 180 plus mirror x
                layoutToAddSref.transFlags = (True,True,layoutToAddSref.transFlags[2])
                layoutToAddSref.rotateAngle = 180.0
            if mirror == "xy":
                #mirror xy = rotate 180
                layoutToAddSref.transFlags = (layoutToAddSref.transFlags[0],True,layoutToAddSref.transFlags[2])
                layoutToAddSref.rotateAngle = 180.0
            if rotate:
                layoutToAddSref.transFlags = (layoutToAddSref.transFlags[0],True,layoutToAddSref.transFlags[2])
                layoutToAddSref.rotateAngle = rotate
                
        #add the sref to the root structure
        
        self.structures[self.rootStructureName].srefs+=[layoutToAddSref]        
        if updateInternalMap:
            #now re-do the hierarchy
            del self.xyTree[:]
            self.populateCoordinateMap()
        
    def addBox(self,layerNumber=0, dataType = 0, purposeNumber=None, offsetInMicrons=(0,0), width=1.0, height=1.0, updateInternalMap=False,center=False):
        """
        Method to add a box to a layout
        """
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        widthInLayoutUnits = self.userUnits(width)
        heightInLayoutUnits = self.userUnits(height)
        if not center:
            coordinates=[offsetInLayoutUnits,
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]),
                         (offsetInLayoutUnits[0]+widthInLayoutUnits,offsetInLayoutUnits[1]+heightInLayoutUnits),
                         (offsetInLayoutUnits[0],offsetInLayoutUnits[1]+heightInLayoutUnits),
                         offsetInLayoutUnits]
        else:
            startPoint = (offsetInLayoutUnits[0]-widthInLayoutUnits/2, offsetInLayoutUnits[1]-heightInLayoutUnits/2)
            coordinates=[startPoint,
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]),
                         (startPoint[0]+widthInLayoutUnits,startPoint[1]+heightInLayoutUnits),
                         (startPoint[0],startPoint[1]+heightInLayoutUnits),
                         startPoint]
        boundaryToAdd = GdsBoundary()
        boundaryToAdd.drawingLayer = layerNumber
        boundaryToAdd.dataType = dataType
        boundaryToAdd.coordinates = coordinates
        boundaryToAdd.purposeLayer = purposeNumber
        #add the sref to the root structure
        self.structures[self.rootStructureName].boundaries+=[boundaryToAdd]
        if updateInternalMap:
            #now re-do the hierarchy
            del self.xyTree[:]
            self.populateCoordinateMap()
    
    def addPath(self, layerNumber=0, purposeNumber = None, coordinates=[(0,0)], width=1.0, updateInternalMap=False):
        """
        Method to add a path to a layout
        """
        widthInLayoutUnits = self.userUnits(width)
        layoutUnitCoordinates = []
        #first convert to proper units
        for coordinate in coordinates:
            cX = self.userUnits(coordinate[0])
            cY = self.userUnits(coordinate[1])
            layoutUnitCoordinates += [(cX,cY)]
        pathToAdd = GdsPath()
        pathToAdd.drawingLayer=layerNumber
        pathToAdd.purposeLayer = purposeNumber
        pathToAdd.pathWidth=widthInLayoutUnits
        pathToAdd.coordinates=layoutUnitCoordinates
        #add the sref to the root structure
        self.structures[self.rootStructureName].paths+=[pathToAdd]
        if updateInternalMap:
            #now re-do the hierarchy
            del self.xyTree[:]
            self.populateCoordinateMap()
        
    def addText(self, text, layerNumber=0, purposeNumber = None, offsetInMicrons=(0,0), magnification=0.1, rotate = None, updateInternalMap=False):
        offsetInLayoutUnits = (self.userUnits(offsetInMicrons[0]),self.userUnits(offsetInMicrons[1]))
        textToAdd = GdsText()
        textToAdd.drawingLayer = layerNumber
        textToAdd.purposeLayer = purposeNumber
        textToAdd.dataType = 0
        textToAdd.coordinates = [offsetInLayoutUnits]
        if(len(text)%2 == 1):
            #pad with a zero
            text = text + '\x00'
        textToAdd.textString = text
        textToAdd.transFlags = (False,False,True)
        textToAdd.magFactor = magnification
        if rotate:
            textToAdd.transFlags = (False,True,True)
            textToAdd.rotateAngle = rotate
        #add the sref to the root structure
        self.structures[self.rootStructureName].texts+=[textToAdd]
        if updateInternalMap:
            #now re-do the hierarchy
            del self.xyTree[:]
            self.populateCoordinateMap()
            
    def isBounded(self,testPoint,startPoint,endPoint):
        #these arguments are touples of (x,y) coordinates
        if testPoint == None:
            return 0
        if(testPoint[0]<=max(endPoint[0],startPoint[0]) and \
           testPoint[0]>=min(endPoint[0],startPoint[0]) and \
           testPoint[1]<=max(endPoint[1],startPoint[1]) and \
           testPoint[1]>=min(endPoint[1],startPoint[1])):
            return 1
        else:
            return 0
        
    def intersectionPoint(self,startPoint1,endPoint1,startPoint2,endPoint2):
        if((endPoint1[0]-startPoint1[0])!=0 and (endPoint2[0]-startPoint2[0])!=0):
            pSlope = (endPoint1[1]-startPoint1[1])/(endPoint1[0]-startPoint1[0])
            pIntercept = startPoint1[1]-pSlope*startPoint1[0]
            qSlope = (endPoint2[1]-startPoint2[1])/(endPoint2[0]-startPoint2[0])
            qIntercept = startPoint2[1]-qSlope*startPoint2[0]
            if(pSlope!=qSlope):
                newX=(qIntercept-pIntercept)/(pSlope-qSlope)
                newY=pSlope*newX+pIntercept
            else:
                #parallel lines can't intersect
                newX=None
                newY=None
        elif((endPoint1[0]-startPoint1[0])==0 and (endPoint2[0]-startPoint2[0])==0):
            #two vertical lines cannot intersect
            newX = None
            newY = None
        elif((endPoint1[0]-startPoint1[0])==0 and (endPoint2[0]-startPoint2[0])!=0):
            qSlope = (endPoint2[1]-startPoint2[1])/(endPoint2[0]-startPoint2[0])
            qIntercept = startPoint2[1]-qSlope*startPoint2[0]        
            newX=endPoint1[0]
            newY=qSlope*newX+qIntercept
        elif((endPoint1[0]-startPoint1[0])!=0 and (endPoint2[0]-startPoint2[0])==0):
            pSlope = (endPoint1[1]-startPoint1[1])/(endPoint1[0]-startPoint1[0])
            pIntercept = startPoint1[1]-pSlope*startPoint1[0]
            newX=endPoint2[0]
            newY=pSlope*newX+pIntercept
        return (newX,newY)
        
    def isCollinear(self,testPoint,point1,point2):
        slope1 = (testPoint[1]-point1[1])/(testPoint[0]-point1[0])
        slope2 = (point2[1]-point1[1])/(point2[0]-point1[0])
        if slope1 == slope2:
            return True
        return False
    
    def doShapesIntersect(self,shape1Coordinates, shape2Coordinates):
        """
        Utility function to determine if 2 arbitrary shapes intersect.
        We define intersection by taking pairs of points in each shape (assuming they are in order)
        and seeing if any of the lines formed by these pais intersect.
        """
        for shape1Index in range(0,len(shape1Coordinates)-1):
            for shape2Index in range(0,len(shape2Coordinates)-1):
                startPoint1 = shape1Coordinates[shape1Index]
                endPoint1 = shape1Coordinates[shape1Index+1]
                startPoint2 = shape2Coordinates[shape2Index]
                endPoint2 = shape2Coordinates[shape2Index+1]
                intersect = self.intersectionPoint(startPoint1,endPoint1,startPoint2,endPoint2)
                if(self.isBounded(intersect,startPoint1,endPoint1) and self.isBounded(intersect,startPoint2,endPoint2)):
                    return True  #these shapes overlap!
        return False #these shapes are ok
    
    def isPointInsideOfBox(self,pointCoordinates,boxCoordinates):
        leftBound = boxCoordinates[0][0]
        rightBound = boxCoordinates[0][0]
        topBound = boxCoordinates[0][1]
        bottomBound = boxCoordinates[0][1]
        for point in boxCoordinates:
            if point[0]<leftBound:
                leftBound = point[0]
            if point[0]>rightBound:
                rightBound = point[0]
            if point[1]<bottomBound:
                bottomBound = point[1]
            if point[1]>topBound:
                topBound = point[1]
        if(pointCoordinates[0]>rightBound or
           pointCoordinates[0]<leftBound or
           pointCoordinates[1]>topBound or
           pointCoordinates[1]<bottomBound):
            return False
        return True
    
    def isShapeInsideOfBox(self,shapeCoordinates, boxCoordinates):
        #go through every point in the shape to test if they are all inside the box
        for point in shapeCoordinates:
            if not self.isPointInsideOfBox(point,boxCoordinates):
                return False
        return True
        
                
    def fillAreaDensity(self, layerToFill = 0, offsetInMicrons = (0,0), coverageWidth = 100.0, coverageHeight = 100.0,
                        minSpacing = 0.22, blockSize = 1.0):
        effectiveBlock = blockSize+minSpacing
        widthInBlocks = int(coverageWidth/effectiveBlock)
        heightInBlocks = int(coverageHeight/effectiveBlock)
        passFailRecord = []
        
        print "Filling layer:",layerToFill
        def isThisBlockOk(startingStructureName,coordinates,rotateAngle=None):
            #go through every boundary and check
            for boundary in self.structures[startingStructureName].boundaries:
                #only test shapes on the same layer
                if(boundary.drawingLayer == layerToFill):
                    #remap coordinates
                    shiftedBoundaryCoordinates = []
                    for shapeCoordinate in boundary.rotatedCoordinates(rotateAngle):
                        shiftedBoundaryCoordinates+=[(shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1])]
                    joint = self.doShapesIntersect(self.tempCoordinates, shiftedBoundaryCoordinates)
                    if joint:
                        self.tempPassFail = False                    
                    common = self.isShapeInsideOfBox(shiftedBoundaryCoordinates,self.tempCoordinates)
                    if common:
                        self.tempPassFail = False
            for path in self.structures[startingStructureName].paths:
                #only test shapes on the same layer
                if(path.drawingLayer == layerToFill):
                    #remap coordinates
                    shiftedBoundaryCoordinates = []
                    for shapeCoordinate in path.equivalentBoundaryCoordinates(rotateAngle):
                        shiftedBoundaryCoordinates+=[(shapeCoordinate[0]+coordinates[0],shapeCoordinate[1]+coordinates[1])]
                    joint = self.doShapesIntersect(self.tempCoordinates, shiftedBoundaryCoordinates)
                    if joint:
                        self.tempPassFail = False                    
                    common = self.isShapeInsideOfBox(shiftedBoundaryCoordinates,self.tempCoordinates)
                    if common:
                        self.tempPassFail = False
        
        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                percentDone = (float((yIndex*heightInBlocks)+xIndex) / (heightInBlocks*widthInBlocks))*100
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                self.tempCoordinates=[(self.userUnits(blockX-minSpacing),self.userUnits(blockY-minSpacing)),
                    (self.userUnits(blockX-minSpacing),self.userUnits(blockY+effectiveBlock)),
                    (self.userUnits(blockX+effectiveBlock),self.userUnits(blockY+effectiveBlock)),
                    (self.userUnits(blockX+effectiveBlock),self.userUnits(blockY-minSpacing)),
                    (self.userUnits(blockX-minSpacing),self.userUnits(blockY-minSpacing))]
                self.tempPassFail = True
                #go through the hierarchy and see if the block will fit
                self.traverseTheHierarchy(delegateFunction = isThisBlockOk)
                #if its bad, this global tempPassFail will be false
                #if true, we can add the block
                passFailRecord+=[self.tempPassFail]
            print "Percent Complete:"+str(percentDone)
                
        passFailIndex=0
        for yIndex in range(0,heightInBlocks):
            for xIndex in range(0,widthInBlocks):
                blockX = (xIndex*effectiveBlock)+offsetInMicrons[0]
                blockY = (yIndex*effectiveBlock)+offsetInMicrons[1]
                if passFailRecord[passFailIndex]:
                    self.addBox(layerToFill, (blockX,blockY), width=blockSize, height=blockSize)
                passFailIndex+=1
        
        print "Done\n\n"