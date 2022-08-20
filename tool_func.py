import glv
from math import *
import numpy as np

#返回nums中第一个>=target的值位置，如果nums中都比target小，则返回len(nums)
def lower_bound(nums, target):
    low, high = 0, len(nums)-1
    pos = len(nums)-1
    while low<high:
        mid = int((low+high)/2)
        if nums[mid] < target:
            low = mid+1
        else:#>=
            high = mid
            #pos = high
    if nums[low]>=target:
        pos = low
    return pos

def blh2xyz(B,L,H):
    sB = sin(B)
    cB = cos(B)
    sL = sin(L)
    cL = cos(L)
    N = glv.a/sqrt(1-glv.e2*sB**2)
    X = (N+H)*cB*cL
    Y = (N+H)*cB*sL
    Z = (N*(1-glv.e2)+H)*sB
    return np.array([X,Y,Z])

def xyz2blh(X,Y,Z):
    bell = glv.a*(1.0-1.0/glv.f)                          
    ss = sqrt(X*X+Y*Y)   
    zps   = Z/ss
    theta = atan( (Z*glv.a) / (ss*glv.b) )
    sin3  = sin(theta) * sin(theta) * sin(theta)
    cos3  = cos(theta) * cos(theta) * cos(theta)
    
    #Closed formula
    B = atan((Z + glv.ep2 * glv.b * sin3) / (ss - glv.e2 * glv.a * cos3))
    L = atan2(Y,X)
    nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(L))
    H = ss/cos(B) - nn

    i=0
    while i<=100:
        nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(B))
        hOld = H
        phiOld = B
        H = ss/cos(B)-nn
        B = atan(zps/(1.0-glv.e2*nn/(nn+H)))
        if abs(phiOld-B) <= 1.0e-11 and abs(hOld-H) <= 1.0e-5:
            # always convert longitude to 0-360
            if L < 0.0 :
                L += 2 * pi
                break

        i+=1

    return np.array([B,L,H])

def xyz2blh_batch(XX,YY,ZZ):
    BB,LL,HH=[],[],[]
    for i in range(len(XX)):
        X,Y,Z=XX[i],YY[i],ZZ[i]
        bell = glv.a*(1.0-1.0/glv.f)                          
        ss = sqrt(X*X+Y*Y)   
        zps   = Z/ss
        theta = atan( (Z*glv.a) / (ss*glv.b) )
        sin3  = sin(theta) * sin(theta) * sin(theta)
        cos3  = cos(theta) * cos(theta) * cos(theta)
        
        #Closed formula
        B = atan((Z + glv.ep2 * glv.b * sin3) / (ss - glv.e2 * glv.a * cos3))
        L = atan2(Y,X)
        nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(L))
        H = ss/cos(B) - nn

        i=0
        while i<=100:
            nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(B))
            hOld = H
            phiOld = B
            H = ss/cos(B)-nn
            B = atan(zps/(1.0-glv.e2*nn/(nn+H)))
            if abs(phiOld-B) <= 1.0e-11 and abs(hOld-H) <= 1.0e-5:
                # always convert longitude to 0-360
                if L < 0.0 :
                    L += 2 * pi
                    break

            i+=1
        BB.append(B)
        LL.append(L)
        HH.append(H)

    return np.array([BB,LL,HH]).T


def xyz2enu(XYZ=[],XYZ_Ref=[]):

    [b,l,h]=xyz2blh(XYZ_Ref[0],XYZ_Ref[1],XYZ_Ref[2])

    r=[XYZ[0]-XYZ_Ref[0], XYZ[1]-XYZ_Ref[1], XYZ[2]-XYZ_Ref[2]]


    sinPhi = sin(b)
    cosPhi = cos(b)
    sinLam = sin(l)
    cosLam = cos(l)

    N = -sinPhi * cosLam * r[0] - sinPhi * sinLam * r[1] + cosPhi * r[2]
    E = -sinLam * r[0] + cosLam * r[1]
    U = +cosPhi * cosLam * r[0] + cosPhi * sinLam * r[1] + sinPhi * r[2]

    return np.array([E,N,U])

def vxyz2enu(VXYZ=[],VXYZ_Ref=[],XYZ_Ref=[]):

    [b,l,h]=xyz2blh(XYZ_Ref[0],XYZ_Ref[1],XYZ_Ref[2])

    v=[VXYZ[0]-VXYZ_Ref[0], VXYZ[1]-VXYZ_Ref[1], VXYZ[2]-VXYZ_Ref[2]]


    sinPhi = sin(b)
    cosPhi = cos(b)
    sinLam = sin(l)
    cosLam = cos(l)

    N = -sinPhi * cosLam * v[0] - sinPhi * sinLam * v[1] + cosPhi * v[2]
    E = -sinLam * v[0] + cosLam * v[1]
    U = +cosPhi * cosLam * v[0] + cosPhi * sinLam * v[1] + sinPhi * v[2]

    return np.array([E,N,U])

def Cne(B,L):
    res=np.mat(np.zeros((3,3)))

    slat = np.sin(B) 
    clat = np.cos(B)
    slon = np.sin(L) 
    clon = np.cos(L)
    res = np.matrix([[ -slon,clon,0 ],
          [ -slat*clon, -slat*slon, clat],
          [  clat*clon,  clat*slon, slat]])
    return res


def Cnb(pitch,roll,yaw):
    sp = np.sin(pitch)
    cp = np.cos(pitch)
    sr = np.sin(roll)
    cr = np.cos(roll)
    sy = np.sin(yaw)
    cy = np.cos(yaw)
    res=np.matrix([[cy*cr - sy*sp*sr, -sy*cp, cy*sr + sy*sp*cr],
                    [sy*cr + cy*sp*sr, cy*cp, sy*sr - cy*sp*cr],
                    [-cp*sr, sp, cp*cr]])
    return res

def diff_enu(t1=[],xyz=[],t2=[],xyz_ref=[]):
	t,E,N,U=[],[],[],[]
	for i in range(len(t1)):
		index=lower_bound(t2,t1[i])
		if abs(t1[i]-t2[index])>1e-2:
			continue
		t.append(t1[i])
		[e,n,u]=xyz2enu(xyz[i],xyz_ref[index])
		E.append(e)
		N.append(n)
		U.append(u)
	# time=np.array(t).T
	diff=np.array([t,E,N,U]).T
	return diff

def diff_vel(t1=[],vel=[],t2=[],vel_ref=[],xyz_ref=[]):
	t,E,N,U=[],[],[],[]
	for i in range(len(t1)):
		index=lower_bound(t2,t1[i])
		if abs(t1[i]-t2[index])>1e-6:
			continue
		t.append(t1[i])
		[e,n,u]=vxyz2enu(vel[i],vel_ref[index],xyz_ref[index])
		# [e,n,u]=vel[i]-vel_ref[index]
		E.append(e)
		N.append(n)
		U.append(u)
	# time=np.array(t).T
	diff=np.array([t,E,N,U]).T
	return diff


def diff_att(t1=[],att=[],t2=[],att_ref=[]):
	t,p,r,y=[],[],[],[]
	for i in range(len(t1)):
		index=lower_bound(t2,t1[i])
		if abs(t1[i]-t2[index])>1e-6:
			continue
		t.append(t1[i])
		[pp,rr,yy]=att[i]-att_ref[index]
		if abs(yy) > 100:
			yy=0
		p.append(pp)
		r.append(rr)
		y.append(yy)
	# time=np.array(t).T
	diff=np.array([t,p,r,y]).T
	return diff
