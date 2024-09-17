GMPbin_capacity = 20 # using global variable to set the capacity
NBbin_capacity = 20  # we can take input here for the capacity
class BillingInfo:
    # This class stores the billing catalogue
    def __init__(self):
        self.prices = {
            "biodegradable" : 0, # price for biodegradable garbage
            "recyclable" : 2,    # price for recyclable garbage
            "non_recyclable" : 5 # price of non_recyclable garbage
        }

class User:
    # This class stores the user information
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.billing_info= {}  # bills will be saved in a form of dictionary

    def warning(self,message):
        # Receives warning from source bin and gives warning to the user
        print(f"Warning for {self.name} ({self.address}): {message}")

    def total_bill(self):
        # Total bill is calculated for a user
        total = sum(self.billing_info.values())
        print(f"Total bill for {self.name} ({self.address}): {total} tk")
        return total
        
    def update_billing_info(self, item_type, cost): # cost is the bill for that garbage type
        # Updates the billing info of a user
        if item_type in self.billing_info:
            self.billing_info[item_type] += cost
        else:
            self.billing_info[item_type] = cost

class SourceBin:
    # Garbage source, one for every user (for this code)
    def __init__(self, capacity, user): # a single source bin is dedicated to a single user
        self.user = user  # to send warning
        self.capacity = capacity 
        self.current_load = 0
        self.gmp = GMP_bin()

    def add_garbage(self, g_type: str,amount = 1):
        self.current_load += amount 
        if self.current_load > self.capacity:
            self.warning()

        elif self.current_load <= self.capacity:
            self.gmp.add_garbage(self,g_type,amount) # sending the garbage to the GMP_bin
            if self.current_load == self.capacity:
                self.warning()
                #flushing the garbage when the maximum capacity is reached
                self.current_load = 0  # the bin will be made empty once the maximum capacity is reached
        
    def warning(self, message = ''):
        # Recieves warning from GMP_bin and gives waning to the user
        self.user.warning("Reduce garbage production") # sending warning to the user
        # message variable contains the warning message recieved from GMP_bin 
      
class GMP_bin:
    # Garbage management plant bin
    def __init__(self):
        self.capacity = GMPbin_capacity
        self.current_load = 0
        self.billing_info = BillingInfo()
        self.b_bin = B_bin()
        self.nb_bin = NB_bin()

    def add_garbage(self,source,g_type,amount = 1):       # source is taken as an argument to keep track
        #Takes garbage from the source bin and updates the billing info of the user of the source 
        self.current_load += amount 
        if self.current_load > self.capacity:
            self.warning(source)
        elif self.current_load <= self.capacity: # of the billing info and give warning to the corresponding user
            if g_type == "biodegradable":
                source.user.update_billing_info("biodegradable", self.billing_info.prices["biodegradable"]*amount) #updating billing catalog for the user of the source
                self.b_bin.add_garbage(amount)  # sending garbage to B_bin
            elif g_type == "recyclable":
                source.user.update_billing_info("recyclable", self.billing_info.prices["recyclable"]*amount)
                self.nb_bin.add_garbage(self,source,g_type,amount) # sending garbage to NB_bin
            elif g_type == "non_recyclable":
                source.user.update_billing_info("non_recyclable", self.billing_info.prices["non_recyclable"]*amount)
                self.nb_bin.add_garbage(self,source,g_type,amount)  # sending the garbage to NB_bin

            if self.current_load == self.capacity:
                self.warning(source)
                #flushing the garbage when the maximum capacity is reached
                self.current_load = 0   

    def warning(self,source, message = ''):
        # Recieves warning from the NB_bin and sends warning to the source bin
        source.warning("Warning from GMP-bin")  # sending the warning to the source
        # message variable contains the warning message recieved from NB_bin 

class NB_bin:
    # Non-biodegradable garbage bin
    def __init__(self):
        self.capacity = NBbin_capacity
        self.current_load = 0
        self.billing_info = BillingInfo()
        self.r_bin = R_bin()
        self.nr_bin = NR_bin()
        
    def add_garbage(self,gmp,source, g_type, amount = 1):
        # Takes non biodegradable garbage from GMP_bin and sends them to the NR and R bin
        self.current_load += amount
        if self.current_load > self.capacity:
            self.warning(gmp,source)
        elif self.current_load <= self.capacity:
            if g_type == "recyclable":
                self.r_bin.add_garbage(amount)
            elif g_type == "non_recyclable":
                self.nr_bin.add_garbage(amount)
            if self.current_load == self.capacity:
                self.warning(gmp,source)
                #flushing the garbage when the maximum capacity is reached
                self.current_load = 0
            
    def warning(self,gmp,source):
        # Takes no messages from other bin but send warning to the GMP_bin if the load reaches maximum capacity
        gmp.warning(source, "Warning from NB-bin")

class B_bin:
    # Biodegradable garbage bin. Has infinite capacity
    def __init__(self):
        self.capacity = float('inf') #infinite capacity
        self.current_load = 0

    def add_garbage(self,amount =1):
        # Takes only biodegradable garbage
        if self.current_load < self.capacity:
            self.current_load += amount

class R_bin:
    # Recyclable garbage bin. Has infinite capacity
    def __init__(self):
        self.capacity = float('inf')
        self.current_load = 0

    def add_garbage(self,amount=1):
        if self.current_load < self.capacity:
            self.current_load += amount

class NR_bin:
    # Non-recyclable garbage bin. Has infinite capacity
    def __init__(self):
        self.capacity = float('inf')
        self.current_load = 0

    def add_garbage(self,amount=1):
        if self.current_load < self.capacity:
            self.current_load += amount
    
# test case
user1 = User('Mushfiq', 'Ahsanullah hall, buet')
user2 = User("Kabbo","Titumir hall, buet")
user3 = User('Nahin', 'Suhrawadry hall, buet')
# Create bins
source_bin1 = SourceBin(10,user1)
source_bin2 = SourceBin(10,user2)
source_bin3 = SourceBin(10,user3)

i=1
while(i<= 9):
    source_bin1.add_garbage("non_recyclable")
    i+=1
user1.total_bill()

source_bin2.add_garbage("recyclable", 10)
user2.total_bill()

i = 1
while (i <= 5):
    source_bin3.add_garbage("biodegradable")
    i+=1
user3.total_bill()

