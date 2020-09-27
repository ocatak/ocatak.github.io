import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.svm import LinearSVC
from graphviz import Source
from sklearn import svm


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
secilecek_kolonlar = ['duration','src_bytes','dst_bytes','wrong_fragment','urgent','hot','num_failed_logins',
'num_compromised','root_shell','su_attempted','num_root','num_file_creations','num_shells',
'num_access_files','num_outbound_cmds','count','srv_count','serror_rate','srv_serror_rate',
'rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count',
'dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate',
'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate',
'dst_host_srv_rerror_rate']

#X = verikumesi[secilecek_kolonlar].as_matrix()
#y = verikumesi['label'].apply(lambda d:0 if d == 'normal.' else 1).as_matrix()

X_normal = verikumesi.query("label == 'normal.' ")[secilecek_kolonlar].as_matrix()
X_malicious = verikumesi.query("label != 'normal.' ")[secilecek_kolonlar].as_matrix()

print(X_normal.shape)


X_normal = X_normal[0:20000,:]
np.random.shuffle(X_malicious)
X_malicious = X_malicious[0:1000,:]

clf = svm.OneClassSVM(nu=0.9, kernel="rbf", degree=8, gamma=10, verbose=True, max_iter=-1)
clf.fit(X_normal)

print('X_normal predict')
y_pred_normal = clf.predict(X_normal)
n_error_normal = y_pred_normal[y_pred_normal == 1].size
print(n_error_normal, X_normal.shape[0])

y_pred_malicious = clf.predict(X_malicious)
n_error_malicious = y_pred_malicious[y_pred_malicious == -1].size
print(n_error_malicious, X_malicious.shape[0])
