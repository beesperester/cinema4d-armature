from examples.leg_shape import leg_shape
from examples.scene import l_upperleg_joint

def main():
    upperleg = leg_shape.Integrate(l_upperleg_joint)

    print(upperleg.lowerleg.weight.GetObject())
