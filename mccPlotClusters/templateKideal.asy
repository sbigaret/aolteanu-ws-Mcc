import settings;
import plain;

outformat="jpg";
int sz = 700;
size(sz,sz);
pen dashed=linetype(new real[] {8,8});
int circle_size = 20;

real  x1,x2,y1,y2,c1_circle_size,c2_circle_size;
for(int i=0;i<no_arcs;++i)
{
	x1 = arcs_x1[i];
	y1 = arcs_y1[i];
	x2 = arcs_x2[i];
	y2 = arcs_y2[i];
	if(arc_type[i] == 0)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0,0,0) + 2,Arrows(20));
	if(arc_type[i] == 1)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0,0,0) + 2,Arrow(20));
	if(arc_type[i] == 2)
		draw((x2,y2)+dir((x2,y2)--(x1,y1))*circle_size--(x1,y1)-dir((x2,y2)--(x1,y1))*circle_size,rgb(0,0,0) + 2,Arrow(20));
	if(arc_type[i] == 3)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*circle_size--(x2,y2)-dir((x1,y1)--(x2,y2))*circle_size,rgb(0,0,0) + 2);
}
for(int i=0;i<no_points;++i)
{
	x1 = points_x[i];
	y1 = points_y[i];
	fill(circle((x1,y1),circle_size),rgb(1,1,1));
	draw(circle((x1,y1),circle_size),rgb(0.0,0.0,0.0)+2);
	label(labels[i],(x1,y1),rgb(0.0,0.0,0.0)+fontsize(24));
}
for(int i=0;i<no_cluster_arcs;++i)
{
	x1 = cluster_arcs_x1[i];
	y1 = cluster_arcs_y1[i];
	x2 = cluster_arcs_x2[i];
	y2 = cluster_arcs_y2[i];
	c1_circle_size = cluster_arcs_z1[i] + 2* circle_size;
	c2_circle_size = cluster_arcs_z2[i] + 2* circle_size;
	if(cluster_arc_type[i] == 0)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*c1_circle_size--(x2,y2)+dir((x2,y2)--(x1,y1))*c2_circle_size,rgb(0,0,0) + 2,Arrows(30));
	if(cluster_arc_type[i] == 1)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*c1_circle_size--(x2,y2)+dir((x2,y2)--(x1,y1))*c2_circle_size,rgb(0,0,0) + 2,Arrow(30));
	if(cluster_arc_type[i] == 2)
		draw((x2,y2)+dir((x2,y2)--(x1,y1))*c2_circle_size--(x1,y1)+dir((x1,y1)--(x2,y2))*c1_circle_size,rgb(0,0,0) + 2,Arrow(30));
	if(cluster_arc_type[i] == 3)
		draw((x1,y1)+dir((x1,y1)--(x2,y2))*c1_circle_size--(x2,y2)+dir((x2,y2)--(x1,y1))*c2_circle_size,rgb(0,0,0) + 2);
}
shipout(bbox(Fill(rgb(1,1,1))));
