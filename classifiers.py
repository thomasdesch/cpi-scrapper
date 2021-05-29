import xlwt
from xlwt import Workbook
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing


df = pd.read_excel('demo.xls')
