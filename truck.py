from package import Package

class Truck:

    def __init__(self, truck_id):
     self.truck_id = truck_id
     self.package_list = []
     self.mileage = 0
     self.current_location = 0
     self.current_destination = 0       #At hub location ID
     self.released = False
     self.distance_to_next_delivery = 0

     #Insert package into package_list if truck isn't already full

    def load_truck(self, pkg: Package):

        if(len(self.package_list) < 16):
            pkg.status = "Loaded on Truck #" + str(self.truck_id)
            self.package_list.append(pkg)
            return "Loaded\n"

        else:
            return "Truck Full \n"
    
    def view_code(self):
        pkg: Package   
        s = ""
        for pkg in self.package_list: 
            s += "|ID: %-2s |Loc ID: %-2s |Address: %-41s |City: %-18s |State: %-6s |Zip: %-5s |Weight: %-2s |Status: %-20s |Deadline: %-18s |\n" % (pkg.ID, pkg.location_id, pkg.address, pkg.city, pkg.state, pkg.zip, pkg.weight, pkg.status, pkg.getDeadline())   
            
        return s