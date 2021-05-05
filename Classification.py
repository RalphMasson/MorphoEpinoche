class Prediction():
    def predict():
        from random import randrange
        labels = ('Male','Female')
        choice = randrange(2)
        if(choice==0):fg='blue'
        if(choice==1):fg='red'
        return labels[choice],fg