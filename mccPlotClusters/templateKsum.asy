import settings;
import plain;

outformat="png";
int sz = 700;
size(sz,sz);
pen dashed=linetype(new real[] {8,8});
int circle_size = 70;

real x1,y1,x2,y2,a1,a2,a3,a4,ct;
pair A1,A2,X,Y;
int k;
string c1;
for(int i=0;i<no_clusters;++i)
{
	x1 = cluster_x[i];
	y1 = cluster_y[i];
	c1 = cluster_name[i];
	draw(circle((x1,y1),circle_size),rgb(0.0,0.0,0.0)+2);
	label(c1,(x1,y1)+dir((0,0)--(x1,y1))*1.3*circle_size,rgb(0.0,0.0,0.0)+fontsize(24));
}
k = 0;
for(int i=0;i<no_clusters;++i)
{
	for(int j=i;j<no_clusters;++j)
	{
		if(i==j)
		{
			x1 = cluster_x[i];
			y1 = cluster_y[i];
			a1 = cluster_i[k];
			a2 = cluster_p1[k];
			a3 = cluster_p2[k];
			a4 = cluster_j[k];
			ct = 0;
			if(a1>0.0) ct = ct+1;
			if(a2>0.0) ct = ct+1;
			if(a3>0.0) ct = ct+1;
			if(a4>0.0) ct = ct+1;
			x1 = x1 - circle_size * 0.6;
			y1 = y1 + circle_size * 0.4 * (ct - 1)/2;
			x2 = x1 + 2 * circle_size * 0.6;
			y2 = y1;
			if(a1>0.0)
			{
				draw((x1,y1)--(x2,y2),rgb(0,0,0) + 2,Arrows(20));
				label(string(a1),((x1,y1)+(x2,y2))/2 + (0,10),rgb(0.0,0.0,0.0)+fontsize(24));
				y1 = y1 - circle_size * 0.4;
				y2 = y1;
			}
			if(a2>0.0)
			{
				draw((x1,y1)--(x2,y2),rgb(0,0,0) + 2,Arrow(20));
				label(string(a2),((x1,y1)+(x2,y2))/2 + (0,10),rgb(0.0,0.0,0.0)+fontsize(24));
				y1 = y1 - circle_size * 0.4;
				y2 = y1;
			}
			if(a3>0.0)
			{
				draw((x2,y2)--(x1,y1),rgb(0,0,0) + 2,Arrow(20));
				label(string(a3),((x1,y1)+(x2,y2))/2 + (0,10),rgb(0.0,0.0,0.0)+fontsize(24));
				y1 = y1 - circle_size * 0.4;
				y2 = y1;
			}
			if(a4>0.0)
			{
				draw((x1,y1)--(x2,y2),rgb(0,0,0) + 2);
				label(string(a4),((x1,y1)+(x2,y2))/2 + (0,10),rgb(0.0,0.0,0.0)+fontsize(24));
			}
			if((a1 == a2) && (a1 == a3) && (a1 == a4) && (a1 == 0.0))
			{
				draw((x1,y1)--(x2,y2),rgb(0,0,0) + 2,Arrows(20));
			}
		}
		else
		{
			x1 = cluster_x[i];
			y1 = cluster_y[i];
			x2 = cluster_x[j];
			y2 = cluster_y[j];
			a1 = cluster_i[k];
			a2 = cluster_p1[k];
			a3 = cluster_p2[k];
			a4 = cluster_j[k];
			ct = 0;
			if(a1>0.0) ct = ct+1;
			if(a2>0.0) ct = ct+1;
			if(a3>0.0) ct = ct+1;
			if(a4>0.0) ct = ct+1;
			X = (x1,y1) + dir((x1,y1)--(x2,y2)) * circle_size * 1.2;
			Y = (x2,y2) + dir((x2,y2)--(x1,y1)) * circle_size * 1.2;
			A1 = X + dir(X--(rotate(90,X)*Y)) * circle_size * 0.4 * (ct-1) / 2;
			A2 = Y + dir(X--(rotate(90,X)*Y)) * circle_size * 0.4 * (ct-1) / 2;
			if(a1>0.0)
			{
				draw(A1--A2,rgb(0,0,0) + 2,Arrows(20));
				if(A1.x < A2.x)
					draw(Label(string(a1),Rotate(dir(A1--A2)),align=LeftSide),A1--A2,rgb(0.0,0.0,0.0)+fontsize(24));
				else draw(Label(string(a1),Rotate(dir(A2--A1)),align=LeftSide),A2--A1,rgb(0.0,0.0,0.0)+fontsize(24));
				A1 = A1 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
				A2 = A2 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
			}
			if(a2>0.0)
			{
				draw(A1--A2,rgb(0,0,0) + 2,Arrow(20));
				if(A1.x < A2.x)
					draw(Label(string(a2),Rotate(dir(A1--A2)),align=LeftSide),A1--A2,rgb(0.0,0.0,0.0)+fontsize(24));
				else draw(Label(string(a2),Rotate(dir(A2--A1)),align=LeftSide),A2--A1,rgb(0.0,0.0,0.0)+fontsize(24));
				A1 = A1 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
				A2 = A2 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
			}
			if(a3>0.0)
			{
				draw(A2--A1,rgb(0,0,0) + 2,Arrow(20));
				if(A1.x < A2.x)
					draw(Label(string(a3),Rotate(dir(A1--A2)),align=LeftSide),A1--A2,rgb(0.0,0.0,0.0)+fontsize(24));
				else draw(Label(string(a3),Rotate(dir(A2--A1)),align=LeftSide),A2--A1,rgb(0.0,0.0,0.0)+fontsize(24));
				A1 = A1 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
				A2 = A2 - dir(X--(rotate(90,X)*Y)) * circle_size * 0.4;
			}
			if(a4>0.0)
			{
				draw(A1--A2,rgb(0,0,0) + 2);
				if(A1.x < A2.x)
					draw(Label(string(a4),Rotate(dir(A1--A2)),align=LeftSide),A1--A2,rgb(0.0,0.0,0.0)+fontsize(24));
				else draw(Label(string(a4),Rotate(dir(A2--A1)),align=LeftSide),A2--A1,rgb(0.0,0.0,0.0)+fontsize(24));
			}
		}
		k = k+1;
	}
}
shipout(bbox(Fill(rgb(1,1,1))));

