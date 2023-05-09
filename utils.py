from pprint import pprint

class Buyer:
    
    def __init__(self, assets, yearlyIncomeAfterTax, yearlyExpensesWithoutHouse, withdrawalRate=0.04):
        
        assert yearlyIncomeAfterTax > yearlyExpensesWithoutHouse, "yearlyIncomeAfterTax cannot be smaller than yearlyExpensesWithoutHouse"
        
        self.assets = assets
        self.yearlyIncomeAfterTax = yearlyIncomeAfterTax
        self.yearlyExpensesWithoutHouse = yearlyExpensesWithoutHouse
        self.withdrawalRate = withdrawalRate
        
    def can_afford_house(self, house):
        
        if house.price * house.down_payment_ratio > self.assets:
            print('buyer does not have enough assets for down payment.')
            return False
            
        if house.yearly_cost + self.yearlyExpensesWithoutHouse > self.yearlyIncomeAfterTax:
            print('buyer cannot afford this house due to high costs, and/or low income.')
            return False
        
        return True
    
    
    def caclulate_enough_number(self, house, house_paid_off=False):
        
        if house_paid_off:
            total_yearly_expenses = self.yearlyExpensesWithoutHouse
        else:
            total_yearly_expenses = self.yearlyExpensesWithoutHouse + house.yearly_cost
        
        return (1 / self.withdrawalRate) * total_yearly_expenses
        
        
    def calculate_years_until_retirement(self, house, economy):
        
        if not self.can_afford_house(house):
            return None
        
        # calculate enough number
        self.enough_number = self.caclulate_enough_number(house)
        print(f"\nYour enough number including the house is ${round(self.enough_number,-5):,.0f}\n")
        
        # we assume the house is bought, and track buyer's net worth every year
        self.assets -= house.price * house.down_payment_ratio
        
        years = 0
        
        while (years <= house.loan_years):
            print(f"assets in year {years} is: ${round(self.assets, -3):,.0f}")
            
            if self.assets > self.enough_number:
                print(f"\nCongrats! You can retire in {years} years.")
                return years

            self.assets *= (1 + economy.investmentReturn)  # yearly investement return
            self.assets += self.yearlyIncomeAfterTax - (house.yearly_cost + self.yearlyExpensesWithoutHouse)  # saving

            years += 1
            
        print(f'\nYou can pay off the house in {years - 1} years.')

        # check whether the assets are enough to retire at this point
        self.enough_number = self.caclulate_enough_number(house, house_paid_off=True)
        house.yearly_cost -= house.mortgage

        print(f'Your enough number after paying off the house is ${round(self.enough_number, -3)}.')

        if self.assets >= self.enough_number:
                print(f"\nCongrats! You can retire in {years} years.")
                return years
                
        while self.assets < self.enough_number:
            print(f"assets in year {years} is: ${round(self.assets, -3):,.0f}")
            
            self.assets *= (1 + economy.investmentReturn)  # yearly investement return
            self.assets += self.yearlyIncomeAfterTax - (house.yearly_cost + self.yearlyExpensesWithoutHouse)  # saving

            if self.assets > self.enough_number:
                print(f"\nCongrats! You can retire in {years} years.")
                return years

            years += 1

            if years > 50:
                print(f"You have to work 50+ years to be able to retire, so it's not recommended that you buy a house this expensive.")
                return years


class Economy:
    
    def __init__(self, investmentReturn, APR, realEstateTax, insuranceRatio):
        
        self.investmentReturn = investmentReturn
        self.APR = APR
        self.realEstateTax = realEstateTax
        self.insuranceRatio = insuranceRatio
        

class House:
    
    def __init__(self, price, economy, down_payment_ratio=0.2, loan_years=30, maintenance_cost_ratio=0.01):
        
        assert down_payment_ratio < 1, "down_payment_ratio should be smaller than 1.0"
        
        self.price = price
        self.economy = economy
        
        self.down_payment_ratio = down_payment_ratio
        self.loan_years = loan_years
        
        self.mortgage = round(self.calculate_yearly_payment(economy.APR), -3)
        self.tax = economy.realEstateTax * self.price
        self.insurance = economy.insuranceRatio * self.price
        self.maintenance_cost = self.price * maintenance_cost_ratio
        
        self.yearly_cost = round(self.mortgage + self.tax + self.insurance + self.maintenance_cost, -3)

        print("House info:")
        pprint(vars(self))
        
    def calculate_yearly_payment(self, APR):
        
        loan = self.price * (1 - self.down_payment_ratio)
        
        yearly_mortage = loan * (APR * (1 + APR) ** self.loan_years) / ((1 + APR) ** self.loan_years - 1)
        
        return yearly_mortage
