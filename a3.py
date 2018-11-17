
# coding: utf-8

# In[2]:


import pyspark
sc = pyspark.SparkContext.getOrCreate()

import random
rdd = sc.parallelize([random.randint(0,10000) for i in range(10000)])
rdd.takeOrdered(10, key=lambda x: -x)

