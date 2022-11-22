#coding:gbk
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.special as special
import itertools
def detBoundaries(params, tol):
    '''This modules attempts to determine an appropriate  rectangular 
    boundaries of the integration region of the multivariate Fox H function.'''
    boundary_range = np.arange(0, 50, 0.05)
    dims = len(params[0])
    boundaries = np.zeros(dims)
    for dim_l in range(dims):
		# ~ zeros(shape, dtype=float, order='C')���أ�������һ��������״�����͵���0�������飻
        points = np.zeros((boundary_range.shape[0], dims))
        points[:, dim_l] = boundary_range
        abs_integrand = np.abs(compMultiFoxHIntegrand(points, params))
        index = np.max(np.nonzero(abs_integrand>tol*abs_integrand[0]))
        boundaries[dim_l] = boundary_range[index]
        # ~ print(boundaries)
    return boundaries

def compMultiFoxHIntegrand(y, params):
    ''' This module computes the complex integrand of the multivariate Fox-H
    function at the points given by the rows of the matrix y.'''
    z, mn, pq, c, d, a, b = params
    m, n = zip(*mn)
    p, q = zip(*pq)
    npoints, dims = y.shape
    # ~ print(dims)
    s = 1j*y
    # Estimating sigma[l]
    # ~ lower = np.zeros(dims)
    # ~ upper = np.zeros(dims)
    # ~ for dim_l in range(dims):
        # ~ if b[dim_l]:
            # ~ bj, Bj = zip(*b[dim_l])
            # ~ bj = np.array(bj[:m[dim_l+1]])
            # ~ Bj = np.array(Bj[:m[dim_l+1]])
            # ~ lower[dim_l] = -np.min(bj/Bj)
        # ~ else:
            # ~ lower[dim_l] = -100
        # ~ if a[dim_l]:
            # ~ aj, Aj = zip(*a[dim_l])
            # ~ aj = np.array(aj[:n[dim_l+1]])
            # ~ Aj = np.array(Aj[:n[dim_l+1]])
            # ~ upper[dim_l] =  np.min((1-aj)/Aj)
        # ~ else:
            # ~ upper[dim_l] = 0    
    # ~ mindist = np.linalg.norm(upper-lower)
    # ~ sigs = 0.5*(upper+lower)
    # ~ for j in range(n[0]):
        # ~ num = 1 - c[j][0] - np.sum(c[j][1:] * lower)
        # ~ cnorm = np.linalg.norm(c[j][1:])
        # ~ newdist = np.abs(num) / cnorm
        # ~ if newdist < mindist:
            # ~ mindist = newdist
            # ~ sigs = lower+ 0.5*num*np.array(c[j][1:])/(cnorm*cnorm)    
    # ~ s += sigs 
    s[:,0].real=0.5;s[:,1].real=0.3
    # ~ print(s)
    # Computing products of Gamma factors on both numeratos and denomerator
    s1 = np.c_[np.ones((npoints, 1)), s] 
    # ~ print(s1)   
    prod_gam_num = prod_gam_denom = 1+0j
    for j in range(n[0]):
		# ~ dot()���ص�����������ĵ��
        prod_gam_num *= special.gamma(1-np.dot(s1,c[j]))
    for j in range(q[0]):
        prod_gam_denom *= special.gamma(1-np.dot(s1,d[j]))
    for j in range(n[0], p[0]):
        prod_gam_denom *= special.gamma(np.dot(s1,c[j]))
    for dim_l in range(dims):
#��0����Сa����1���Ǵ�A
        for j in range(n[dim_l+1]):
            prod_gam_num *= special.gamma(1 - a[dim_l][j][0] - a[dim_l][j][1]*s[:, dim_l])
        for j in range(m[dim_l+1]):
            prod_gam_num *= special.gamma(b[dim_l][j][0] + b[dim_l][j][1]*s[:, dim_l])
        for j in range(n[dim_l+1], p[dim_l+1]):
            prod_gam_denom *= special.gamma(a[dim_l][j][0] + a[dim_l][j][1]*s[:, dim_l])
        for j in range(m[dim_l+1], q[dim_l+1]):
            prod_gam_denom *= special.gamma(1 - b[dim_l][j][0] - b[dim_l][j][1]*s[:, dim_l])
    # Final integrand   np.power: �����Ԫ�طֱ���n�η���x2���������֣�Ҳ���������飬����x1��x2������Ҫ��ͬ��axis1�г˻�** ����˷�
    zs=np.power(z,-s)
    result=(prod_gam_num/prod_gam_denom)*np.prod(zs,axis=1)/(2*np.pi)**dims
    #the complex j is not forgotten!
    return result
#��������������������ĺ�����������
def compMultiFoxH(params, nsubdivisions, boundaryTol=0.0001):
    '''This module estimates a multivariate integral using simple rectangule 
    quadrature. In most practical applications, 20 points per dimension provided
    sufficient accuracy.
    Inputs:
    'params': list containing z, mn, pq, c, d, a, b.
    'nsubdivisions': the number of divisions taken along each dimension. Note
    that the total number of points will be nsubdivisions**dim.
    'boundaryTol': tolerance used for determining the boundaries
    Output:
    'result': the estimated value of the multivariate Fox H function...'''
#���ú���������������
    boundaries = detBoundaries(params, boundaryTol)
#�������boundaries��������dim
    dim = boundaries.shape[0]
#list:��Ԫ��ת��Ϊ�б�
    signs = list(itertools.product([1,-1], repeat=dim))
    # ~ print(signs)
#product:����ȡ��list1��ÿ1��Ԫ��,��list2�е�ÿ1��Ԫ��,���Ԫ��,������Ԫ����ϳ�һ���б���
    code = list(itertools.product(range(int(nsubdivisions/2)), repeat=dim))
    # ~ print(code)
    quad = 0
    res = np.zeros((0))
    for sign in signs:
        points = np.array(sign)*(np.array(code)+0.5)*boundaries*2/nsubdivisions
        # ~ print(points)
        res = np.r_[res,np.real(compMultiFoxHIntegrand(points, params))]
        quad += np.sum(compMultiFoxHIntegrand(points, params))
    volume = np.prod(2*boundaries/nsubdivisions)
    result = quad*volume
    return result
def erxiang(n,m):
	result=special.gamma(n+1)/(special.gamma(m+1)*special.gamma(n-m+1))
	return result
def taoF1(n):
	w=55
	A = []
	for k in range(n):
		for l in range(k):
			for nn in range(w):
				MG=compMultiFoxH([[(1/K)*m11*m12],[[0,0],[2,1]],[[0,0],[1,2]],[],[],[[[1-j1+2*l1-k1+2*n1,1]]],[[[m11,1],[m12,1]]]],200,boundaryTol=0.0001);
				T=erxiang(k,l)*erxiang(n,k)*((-1)^(2*nn+2*l-k))*((delta/2)^(2*nn+2*l))*(special.gamma(w+nn)/(special.gamma(1+nn)*special.gamma(w-nn+1)*special.gamma(2*1-k+1+nn)))*(w^(1-2*nn))*MG
	result=T
	return result

    #������ֵ
m11=m12=m21=m22=5
K=1
delta=0.5
gamma=10
yi1=yi2=math.sqrt((gamma/(2*(K+1))))
z=np.arange(0,10,2)
w=55

A = []
l=0
ga0[0]=0.01
print(ga0)

#����
for k in range(len(m1)):
	for j in range(len(ms1)):
		S=special.gamma(m1[k])*special.gamma(ms1[j])*special.gamma(m2[k])*special.gamma(ms2[j])
		# ~ print('S=',S)
		for i in range(len(ga0)):
			x1=(ga1*(ms1[j]-1))/(m1[k]*ga0[i])
			x2=(ga2*(ms2[j]-1))/(m2[k]*ga0[i])
			# ~ x1=(m1*ga0[i])/(ga1*(ms1-1))
			# ~ x2=(m2*ga0[i])/(ga2*(ms2-1))
			# ~ x1=round(x1,4)
			# ~ x2=round(x2,4)
			# ~ H=compMultiFoxH([[x1,x2],[[0,0],[1,2],[1,2]],[[0,1],[2,1],[2,1]],[],[[0,1,1]],[[[1,1],[1-ms1,1]],[[1,1],[1-ms2,1]]],[[[m1,1]],[[m2,1]]]],300,boundaryTol=0.0001);
			H=compMultiFoxH([[x1,x2],[[0,0],[2,1],[2,1]],[[1,0],[1,2],[1,2]],[[1,1,1]],[],[[[1-m1[k],1]],[[1-m2[k],1]]],[[[0,1],[ms1[j],1]],[[0,1],[ms2[j],1]]]],200,boundaryTol=0.0001);
			A.append((H/S).real)
			jg=open(r'C:\Users\Hongyang_Du\Desktop\Python����\CDF\CDF.txt','a')
			jg.write(str((H/S).real)+',')
			jg.close()
		print(m1[k],ms1[j],'finish!')
		jg=open(r'C:\Users\Hongyang_Du\Desktop\Python����\CDF\CDF.txt','a')
		jg.write('\n')
		jg.close()

# ~ m1=5;m2=5
# ~ ms1=5;ms2=5
# ~ ga1=10;ga2=10
# ~ x1=(m1)/(ga1*(ms1-1))
# ~ x2=(m2)/(ga2*(ms2-1))
# ~ A=[1,2,3,4,5,6,7,8,9,10]
# ~ for i in range(10):
	# ~ H=compMultiFoxH([[x1,x2],[[0,1],[1,2],[1,2]],[[1,0],[2,1],[2,1]],[[1-A[i],-1,-1]],[],[[[1,1],[1-ms1,1]],[[1,1],[1-ms2,1]]],[[[m1,1]],[[m2,1]]]],100,boundaryTol=0.00001);	
	# ~ S=special.gamma(1+A[i])*special.gamma(m1)*special.gamma(ms1)*special.gamma(m2)*special.gamma(ms2)
	# ~ C=-1/A[i]*math.log(A[i]*(H/S).real,2)
	# ~ print(C);

#compMultiFoxH�ĸ�ʽ˵��
#z�ĸ�ʽ:��ά��������м�����;�˴��Զ�άΪ��
#[2,3];
#mn or pq�ĸ�ʽ��������[]Ϊ���壬�����ٷ�С[]��ÿһ��С[]����һ��mn��pq��;�˴��Զ�άΪ������һ��С[]Ϊ��mn����Ӧ��������С[]
#[[2,3],[2,3],[4,5]];
#c or d�ĸ�ʽ��������[]Ϊ���壬ÿһ��С[]����һ��(ά)c(d),С[]�ڣ���һ����Ϊc,ʣ�µ�������ΪC��
#[[2,1,1],[5,4,3]];
#a or b�ĸ�ʽ��������[]Ϊ���壬ÿһ��С[]����һά��ÿһά�������N��СС[]��ÿһ��СС[]����������������һ����a���ڶ�����A
#[[[2,3],[4,5]],[[2,3]]]
#��������Щ[]����һ�������[]��ö��Ÿ����ͺ���~~
#*******************һ��ʵ��*****************************************
# ~ [0.5,0.5]
# ~ [[0,0],[2,1],[2,1]]
# ~ [[1,0],[1,2],[1,2]]
# ~ [[1,1,1]]
# ~ []
# ~ [[[-1,1]],[[-1,1]]]
# ~ [[[0,1],[5,1]],[[0,1],[5,1]]]
#���~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#[[0.5,0.5],[[0,0],[2,1],[2,1]],[[1,0],[1,2],[1,2]],[[1,1,1]],[],[[[-1,1]],[[-1,1]]],[[[0,1],[5,1]],[[0,1],[5,1]]]]
