class Prediction():
    def predict():
        from random import randrange,uniform
        labels = ('Male','Female')
        # choice = randrange(2)
        p = uniform(0,1)
        if(p>0.5):
            fg='blue'
            choice = 0
            p = p
        if(p<0.5):
            fg='red'
            choice = 1
            p = 1 - p
        return labels[choice],fg,p