import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

pd.set_option('display.width', 350)


# veri kumesini oku
kolon_adlari = ['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent',
'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root','num_file_creations',
'num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest_login','count','srv_count',
'serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate','srv_diff_host_rate',
'dst_host_count','dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate',
'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate',
'dst_host_srv_rerror_rate','label']

verikumesi = pd.read_csv("kddcup99.tar.gz",compression="gzip", names=kolon_adlari, 
low_memory=False, skiprows=1)

# ilgili kolonlari sec
secilecek_kolonlar = ['serror_rate','srv_serror_rate',
'rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count',
'dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate',
'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate',
'dst_host_srv_rerror_rate']


X = verikumesi[secilecek_kolonlar].as_matrix()
y = verikumesi['label'].apply(lambda d:0 if d == 'normal.' else 1).as_matrix()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

lambdas = [10**-15, 10**-10, 10**-8, 0.0001, 0.001, 0.01, 1, 5, 10, 20, 50, 100, 1000]

col = ['lambda','MSE_Train','MSE_Test','w_0'] + ['w_%d'%i for i in range(1,X.shape[1]+1)] 
ind = ['%d'%i for i in range(1,len(lambdas)+1)]
coef_matrix_simple = pd.DataFrame(index=ind, columns=col)

i = 0
for l in lambdas:
    
    clf = LogisticRegression(penalty='l2', C=1/l)
    clf.fit(X_train,y_train)
    
    y_hat_train = clf.predict(X_train)
    mse_train = mean_squared_error(y_train, y_hat_train)
    
    y_hat_test = clf.predict(X_test)
    mse_test = mean_squared_error(y_test, y_hat_test)
    
    coef_matrix_simple.iloc[i,0] = l
    coef_matrix_simple.iloc[i,1] = mse_train
    coef_matrix_simple.iloc[i,2] = mse_test
    coef_matrix_simple.iloc[i,3] = clf.intercept_[0]
    coef_matrix_simple.iloc[i,4:] = clf.coef_
    i += 1
    os.system('cls' if os.name=='nt' else 'clear')
    print('*'*200)
    print(coef_matrix_simple)

