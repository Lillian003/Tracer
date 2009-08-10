import unittest
import numpy as N
import math

from tracer_engine import TracerEngine
from ray_bundle import RayBundle
from spatial_geometry import general_axis_rotation
from spatial_geometry import generate_transform
from sphere_surface import SphereSurface
from boundary_shape import BoundarySphere
from flat_surface import FlatSurface
from receiver import Receiver
from object import AssembledObject
from assembly import Assembly
import assembly
from paraboloid import Paraboloid
import pdb


class TestTree(unittest.TestCase):
    """Tests an assembly composed of objects"""
    def setUp(self):
        self.assembly = Assembly()

        surface1 = FlatSurface(location=N.array([0,0,0.]), width=10., height=10.)
        self.object1 = AssembledObject()
        self.object1.add_surface(surface1)  

        surface3 = SphereSurface(radius=2.)
        boundary = BoundarySphere(location=N.r_[0,0.,3], radius=3.)
        self.object2 = AssembledObject()
        self.object2.add_surface(surface3)
        self.object2.add_boundary(boundary)

        self.transform1 = generate_transform(N.r_[1.,0,0],N.pi/4,N.c_[[0,0,-1.]])
        self.transform2 = generate_transform(N.r_[0,0.,0],0.,N.c_[[0.,0,2]])
        self.assembly.add_object(self.object1, self.transform1)
        self.assembly.add_object(self.object2, self.transform2)
      
    def test_tree1(self):
        """Tests that the tracing tree works, with three rays"""
        x = 1./(math.sqrt(2))
        dir = N.c_[[0,x,x],[0,-x,x],[0,0,1.]]
        position = N.c_[[0,0,2.],[0,0,2.],[0,0.,2.]]

        bund = RayBundle()
        bund.set_vertices(position)
        bund.set_directions(dir)
        bund.set_energy(N.r_[[1.,1.,1.]])
        bund.set_ref_index(N.r_[[1.,1.,1.]])

        self.engine = TracerEngine(self.assembly)

        self.engine.ray_tracer(bund,3,.05)[0]
        params = self.engine.get_parents_from_tree()
        correct_params = [N.r_[0,1,2],N.r_[1,2],N.r_[0]]
        N.testing.assert_equal(params, correct_params)

    def test_tree2(self):
        """Tests that the tracing tree works, with a new set of rays"""
        x = 1./(math.sqrt(2))
        position = N.c_[[0,0.,-5.],[0,0.,2.],[0,2.,-5.],[0,0.,0],[0,0,2.]]
        dir = N.c_[[0,0,1.],[0,x,-x],[0,0,-1.],[0,0,1.],[0,-x,x]]
        
        bund = RayBundle()
        bund.set_vertices(position)
        bund.set_directions(dir)
        bund.set_energy(N.r_[[1.,1.,1.,1,1.]])
        bund.set_ref_index(N.r_[[1.,1.,1.,1,1.]])

        self.engine = TracerEngine(self.assembly)

        self.engine.ray_tracer(bund,3,.05)[0]
        params = self.engine.get_parents_from_tree()
        correct_params = [N.r_[0,1,3,4],N.r_[2,3,1],N.r_[2,1]]
        N.testing.assert_equal(params, correct_params)

class TestTree2(unittest.TestCase):
    """Tests the tracing tree with a refractive surface"""  
    def setUp(self):
        self.assembly = Assembly()

        surface1 = FlatSurface(location=N.array([0,0,-1.]), width=5., height=5., mirror=False)
        surface2 = FlatSurface(location=N.array([0,0,1.]), width=5., height=5., mirror=False)
        self.object1 = AssembledObject()
        self.object1.add_surface(surface1)
        self.object1.add_surface(surface2)
        self.object1.set_ref_index([surface1, surface2], 1.5)

        surface3 = SphereSurface(radius=2.)
        boundary = BoundarySphere(location=N.r_[0,0.,3], radius=3.)
        self.object2 = AssembledObject()
        self.object2.add_surface(surface3)
        self.object2.add_boundary(boundary)

        self.transform = generate_transform(N.r_[0,0.,0],0.,N.c_[[0.,0,2]])
        self.assembly.add_object(self.object1)
        self.assembly.add_object(self.object2, self.transform)

        x = 1./(math.sqrt(2))
        dir = N.c_[[0,1.,0.],[0,x,x],[0,0,1.]]
        position = N.c_[[0,0,2.],[0,0,2.],[0,0.,2.]]

        self._bund = RayBundle()
        self._bund.set_vertices(position)
        self._bund.set_directions(dir)
        self._bund.set_energy(N.r_[[1.,1.,1.]])
        self._bund.set_ref_index(N.r_[[1.,1.,1.]])

        self.engine = TracerEngine(self.assembly)

    def test_assembly3(self):
        """Tests the assembly after three iterations"""
        self.engine.ray_tracer(self._bund,3,.05)[0]
        params = self.engine.get_parents_from_tree()
        correct_params = [N.r_[1,2],N.r_[0,1,0],N.r_[0,1]]
        N.testing.assert_equal(params, correct_params)


if __name__ == '__main__':
    unittest.main()
