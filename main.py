import math

class Section:
    f_ab = 0
    f_ac = 0
    f1 = 0
    f2 = 0
    f3 = 0
    theta = 0
    isFinal = bool(False)
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
    sections = []
    def __init__(self, section_count, total_length, total_height):
        member_length = total_length / section_count
        section_length = total_height + member_length + math.sqrt(member_length**2 + total_height**2)
        bottom_length = total_length - member_length
        truss_length = section_count * section_length + bottom_length
        angle = math.atan(total_height / member_length)
        prev_section = Section(r1x, r1y, r2x, angle)
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


#User input (in)
total_length = 240
total_height = 24

#Material Properties (lb/in^3,psi)
density = 0.2834
youngs_modulus = 2.9e7
yield_strength = 60200

#Loading (lbs)
force_in = -250


#Calculate Reactionary Forces r1x, r1y, r2x
r1x = force_in * (total_length / total_height)
r1y = -1 * force_in
r2x = -1 * force_in * (total_length / total_height)

#Opimize for Number of sections number of sections will be from 2 to 20  
section_count = 2

for truss_section_count in range(2, section_count +1):
    new_truss = Truss(truss_section_count, total_length, total_height)
    print(new_truss.forces())

#print(section1.forces())
#print(section2.forces())