import settings;
import plain;

outformat="png";
int sz = 700;
size(sz,sz);
pen dashed=linetype(new real[] {8,8});
int circle_size = 20;

real  x1,x2,y1,y2;
int ct = 0;
if(no_obj > 1)
{
	for(int i=0;i<no_obj-1;++i)
	{
		for(int j=i+1;j<no_obj;++j)
		{
			x1 = obj_x[i];
			y1 = obj_y[i];
			x2 = obj_x[j];
			y2 = obj_y[j];
			if(arc_type[ct] == 0)
			{
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0.3,0,0.3));
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x1,y1)+dir((x1,y1)--(x2,y2))*circle_size * 3,rgb(0.3,0,0.3) + 3);
				draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size * 3--(x2,y2)+dir((x2,y2)--(x1,y1))*circle_size,rgb(0.3,0,0.3) + 3);
			}
			if(arc_type[ct] == 1)
			{
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0.3,0,0.3));
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x1,y1)+dir((x1,y1)--(x2,y2))*(circle_size * 3 - 15),rgb(0,0,1) + 3);
				draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size * 3--(x2,y2)+dir((x2,y2)--(x1,y1))*(circle_size + 15),rgb(1,0,0) + 3);
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x1,y1)+dir((x1,y1)--(x2,y2))*circle_size * 3,rgb(0,0,1),Arrow(20));
				draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size * 3--(x2,y2)+dir((x2,y2)--(x1,y1))*circle_size,rgb(1,0,0),Arrow(20));
			}
			if(arc_type[ct] == 2)
			{
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0.3,0,0.3));
				draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size--(x2,y2)+dir((x2,y2)--(x1,y1))*(circle_size * 3 - 15),rgb(0,0,1) + 3);
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size * 3--(x1,y1)+dir((x1,y1)--(x2,y2))*(circle_size + 15),rgb(1,0,0) + 3);
				draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size--(x2,y2)+dir((x2,y2)--(x1,y1))*circle_size * 3,rgb(0,0,1),Arrow(20));
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size * 3--(x1,y1)+dir((x1,y1)--(x2,y2))*circle_size,rgb(1,0,0),Arrow(20));
			}
			if(arc_type[ct] == 3)
				draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0,0,0)+2);
			ct = ct + 1;
		}
	}
}
for(int i=0;i<no_obj;++i)
{
	x1 = obj_x[i];
	y1 = obj_y[i];
	fill(circle((x1,y1),circle_size),rgb(1,1,1));
	draw(circle((x1,y1),circle_size),rgb(0.0,0.0,0.0)+2);
	label(labels[i],(x1,y1),rgb(0.0,0.0,0.0)+fontsize(24));
}
shipout(bbox(Fill(rgb(1,1,1))));
