import bpy, bmesh
from bpy.types import Node
from ... mn_node_base import AnimationNode
from ... mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling
from ... data_structures.mesh import *

class mn_SetCurveOnObject(Node, AnimationNode):
    bl_idname = "mn_SetCurveOnObject"
    bl_label = "Set Curve on Object"
    
    def init(self, context):
        forbidCompiling()
        socket = self.inputs.new("mn_ObjectSocket", "Object")
        socket.showName = False
        self.inputs.new("mn_BezierCurveSocket", "Curve")
        self.outputs.new("mn_ObjectSocket", "Object")
        allowCompiling()
        
    def draw_buttons(self, context, layout):
        pass
        
    def getInputSocketNames(self):
        return {"Object" : "object",
                "Curve" : "curve"}
    def getOutputSocketNames(self):
        return {"Object" : "object"}
        
    def execute(self, object, curve):
        if object is None: return object
        if object.type == "CURVE":
            if object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode = "OBJECT")
            if object.mode == "OBJECT":
                data = object.data
                data.splines.clear()
                for spline in curve.splines:
                    bSpline = data.splines.new("BEZIER")
                    bSpline.use_cyclic_u = spline.isCyclic
                    bSpline.bezier_points.add(len(spline.points)-1);
                    for i, point in enumerate(spline.points):
                        bPoint = bSpline.bezier_points[i]
                        bPoint.co = point.location
                        bPoint.handle_left = point.leftHandle
                        bPoint.handle_right = point.rightHandle
        return object