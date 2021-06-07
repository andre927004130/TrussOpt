import math

class Section:
    def __init__(self, force1, force2, force3, angle, isFinal = bool(False)):
        self.f1 = self.f_ab = force1
        self.f2 = self.f_ac = force2
        self.f3 = force3
        self.angle = angle
        self.isFinal = isFinal

    def f_cb(self):
        return self.f_ac/(math.sin(self.angle)) 
    def f1_next(self):
        return self.f_ab + self.f_cb() * (math.cos(self.angle))
    def f2_next(self):
        return self.f_cb() * (math.sin(self.angle)) * -1
    def f3_next(self):
        return self.f_cb() * (math.cos(self.angle)) * -1 + self.f3
    def forces(self):
        if self.isFinal:
            return abs(self.f_ab), abs(self.f_ac),-1 * abs(self.f_cb())
        else:
            return abs(self.f_ab), abs(self.f_ac),-1 * abs(self.f_cb()), -1 * abs(self.f3_next())

class Truss:
    def __init__(self, section_count, total_length, total_height):
        self.member_length = total_length / section_count
        section_length = total_height + self.member_length + math.sqrt(self.member_length**2 + total_height**2)
        bottom_length = total_length - self.member_length
        self.truss_length = section_count * section_length + bottom_length
        
        #Calculate Reactionary Forces r1x, r1y, r2x, and angle
        r1x = force_in * (total_length / total_height)
        r1y = -1 * force_in
        r2x = -1 * force_in * (total_length / total_height)
        angle = math.atan(total_height / self.member_length)

        prev_section = Section(r1x, r1y, r2x, angle)
        self.sections = []
        self.sections.append(prev_section)
        for current_section_count in range(2, section_count+1):
            isFinal = current_section_count == section_count 
            prev_section = Section(prev_section.f1_next(), prev_section.f2_next(), prev_section.f3_next(), angle, isFinal)
            self.sections.append(prev_section)
    def forces(self):
        forces = []
        for section in self.sections:
            forces += section.forces()
        return forces

class TrussWeightOptimizer:
    def __init__(self, density, youngs_modulus, yield_strength, min_cross_section, truss):
        self.density = density
        self.youngs_modulus = youngs_modulus
        self.yield_strength = yield_strength
        self.min_cross_section = min_cross_section
        self.max_cross_section = 100
        self.truss = truss
    def fos(self, force, area, inertia):
        fos_axial = self.yield_strength * (area / force)
        fos_buckle = (math.pi)**2 * self.youngs_modulus * inertia / (force * self.truss.member_length**2)
        if force < 0:
            return min(fos_axial, fos_buckle)
        else:
            return fos_axial
    
    def hasAcceptableFOS(self,area,inertia):
        for force in self.truss.forces():
            fos = self.fos(force, area, inertia)
            if abs(fos) < 1.5:
                return bool(False)
        return bool(True)

    def optimal_cross_section(self):
        cross_section = self.min_cross_section
        while(cross_section < self.max_cross_section):
            area = cross_section**2
            inertia = cross_section**4 / 12
            optimal_weight = 0
            
            if self.hasAcceptableFOS(area, inertia):
                return self.truss.truss_length * area * self.density, cross_section
            cross_section += .0625

            

#User input (in)
total_length = int(input("Enter the total truss length in inches:"))
total_height = int(input("Enter the total truss height in inches:"))

#Material Properties (lb/in^3,psi)
density = 0.2834
youngs_modulus = 2.9e7
yield_strength = 60200

#Loading (lbs)
force_in = int(input("Enter the applied load value in lbs (+/-):"))

#Opimize for Number of sections number of sections will be from 2 to 20  
section_count = 20
truss_cross_sections = {}
truss_weights_list = {}
for truss_section_count in range(2, section_count +1):
    new_truss = Truss(truss_section_count, total_length, total_height)
    trussOptimizer = TrussWeightOptimizer(density, youngs_modulus, yield_strength, .0625, new_truss)
    truss_cross_sections[trussOptimizer.optimal_cross_section()] = new_truss
    truss_weights_list [trussOptimizer.optimal_cross_section()] = "Number of sections:", truss_section_count

lightest_truss_weight = -1
for cross, truss in truss_cross_sections.items():
    (weight, cross_section_length) = cross
    if lightest_truss_weight < 0 or weight < lightest_truss_weight:
        lightest_truss_weight = weight
        lightest_truss_cross = cross_section_length
        lightest_truss = truss

print("Weight of lightest truss (lbs):", lightest_truss_weight)
print("Member cross-section width (in):", lightest_truss_cross)
print("List of all internal truss forces (lbs):", lightest_truss.forces())
print("Number of sections in lightest truss:",len(lightest_truss.sections))
print(truss_weights_list)
