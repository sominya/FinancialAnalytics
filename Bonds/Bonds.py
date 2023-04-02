from scipy.optimize import newton
class Bonds:
    '''
    Purpose: Create a Bonds object and calculate various properties like
    Bond market value
    Yield to maturity
    Coupon Payments
    Zero coupon bonds
    
    The inputs required -
    face_val - Face value of the bond
    years_to_maturity 
    annual coupon_rate
    coupon_payment_periods - 2 for semi annual, 4 for quaterly , 12 for monthly , 1 for annual
    Example -
    1. zero coupon bond
    b1=Bonds(1000, 20, bond_market_price=455)
    b1.set_coupon_payment()
    b1.set_bond_market_vakue()
    b1.set_yield_to_maturity()

    2. Coupon bond semi annual
    b2 = Bonds(1000, 3, .12,2, bond_sale_price=1124.96)
    b2.set_coupon_payment()
    b2.set_yield_to_maturity()

    '''
    def __init__(self, 
                 face_val, 
                 years_to_maturity, 
                 coupon_rate=0, 
                 coupon_payment_periods=0, 
                 yield_to_maturity=None,
                 bond_sale_price=None
                 ):
        self.face_val = face_val
        self.years_to_maturity = years_to_maturity
        self.coupon_rate = coupon_rate
        self.coupon_payment_periods = coupon_payment_periods
        self.yield_to_maturity = yield_to_maturity
        self.bond_sale_price = bond_sale_price

        if (bond_sale_price is None) & (yield_to_maturity is None):
            raise ValueError('Either the bond_sale_price or the yield_to_maturity must be set both cant be null')
        
        self.set_coupon_payment()
        self.set_yield_to_maturity()
        self.set_bond_market_vakue()
        
        
    def annuity_discount_factor(self, discount_rate ,periods):
        '''
        Calculates Annuity Discount Factor in case calculating discounted cashflows
        '''
        ADF = 0
        if periods>0:
            for i in range(periods):
                ADF += 1/pow((1+discount_rate),i+1)
        return ADF


    def set_coupon_payment(self):
        '''
        Coupon payments in case non-zero coupon bonds
        '''
        if self.coupon_rate > 0 :
            coupon_payment = self.face_val * (self.coupon_rate/self.coupon_payment_periods)
            self.coupon_payment = coupon_payment
        else:
            self.coupon_payment = 0
        print('Coupon Payment per period is: ', self.coupon_payment)
    
    def set_yield_to_maturity(self):
        '''
        Calculate yield to maturity and sets it as an attribute
        This is done by discounting future cashflows from the sale_price
        '''
        ## When there is a coupon payment
        if (self.yield_to_maturity is None) & (self.coupon_rate > 0) :
            def to_minimize(r):
                face_val=self.face_val
                coupon=self.coupon_payment
                periods=self.years_to_maturity*self.coupon_payment_periods
                ADF = self.annuity_discount_factor((r/self.coupon_payment_periods), periods)
                discount_fv = (face_val/pow(1+(r/self.coupon_payment_periods),periods)) + (coupon*ADF)
                sale_price = self.bond_sale_price
                
                # Below function needs to be mimized to zero
                
                return sale_price - discount_fv
            # yield_to_maturity is calculated using the newton raphson optimization of the equation
            self.yield_to_maturity=newton(to_minimize, x0=0.5)
        
        # When no coupon is paid the equation to solve is much simpler
        elif (self.yield_to_maturity is None) & (self.coupon_rate == 0) :
            periods = self.years_to_maturity
            self.yield_to_maturity = pow((face_val/self.bond_sale_price),1/periods)-1
        print('The yield to maturity of this bond is: ', self.yield_to_maturity)
    
    def get_yield_to_maturity(self):
        return self.years_to_maturity
    
    def set_bond_market_vakue(self):
        '''
        If the bond market price is none then calculates and sets the bond market value
        this can be used to calculate whether the bond is worth purchasing
        '''
        discount_rate = self.yield_to_maturity
        if (self.coupon_rate > 0) :
            # Discounted face value
            face_value_discounted = self.face_val/pow((1+(discount_rate/self.coupon_payment_periods)), self.years_to_maturity*self.coupon_payment_periods)

            # Annuity discounted factor to calculate coupon payment discounted
            adf = self.annuity_discount_factor(discount_rate/self.coupon_payment_periods, self.coupon_payment_periods*self.years_to_maturity)
            coupon_value_discounted = adf*self.coupon_payment
            self.bond_market_value = face_value_discounted + coupon_value_discounted
        
        else:
            self.bond_market_value = self.face_val/pow(1+discount_rate,self.years_to_maturity)
        
        print('The current market value of the bond is :', self.bond_market_value)
    
    def get_bond_market_value(self):
        return self.bond_market_value
