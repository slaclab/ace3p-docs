# ParaView recipes

Step-by-step procedures for the ParaView tasks that come up most often with ACE3P results. They assume the [SLAC toolbar](paraview.md#enable-the-slac-toolbar) is loaded and refer to ParaView 5.11, the version installed on Perlmutter and S3DF. Everything the toolbar does can also be done through the normal ParaView menus.

!!! note "Source"
    Adapted from *Accelerator Visualization Recipes for ParaView* by Greg Schussman and Rich Lee, the page linked from the CW23 materials. Menu and filter names have been updated from ParaView 3.8 to 5.11; the sections on the retired Franklin and Lens clusters are replaced by the pointer to NERSC's client-server guide at the end.

## Load data and choose a display style

Click the **SLAC folder** icon. The dialog takes the mesh file (`.ncdf`), optionally one or more field files (`.mod`) and a particle file. On **OK** the other toolbar icons become active for the data you loaded.

Three buttons set how the mesh is drawn:

| Button | Shows |
|---|---|
| Show Mesh as Solid Surface | Opaque surface |
| Show Mesh as Solid with Wireframe | Surface with element edges in black |
| Show Wireframe Front and Solid Back | Outward faces as wireframe, inward faces solid, so you can see inside whichever way the model is turned |

The **e** and **b** buttons color the surface by electric or magnetic field magnitude. **Toggle Show Particles** shows loaded particles as white dots; since particles are inside the mesh, use the wireframe-front style to see them. **Make a plot of the field along the Z axis** opens a line chart of the displayed field along the axis.

To see the field inside the volume rather than on the walls, enable **Read Internal Volume** on the reader as described on the [ParaView page](paraview.md#seeing-the-field-inside-the-volume).

## Clip and slice

Both filters are on the Common toolbar and under **Filters, then Alphabetical**.

- **Clip** removes one side of a plane (or box, or sphere) so you look into the model. Drag the plane widget in the view or type **Origin** and **Normal**, then **Apply**. Uncheck **Show Plane** once it is placed.
- **Slice** keeps only the cut surface, with the field interpolated onto it. Use it on **Entire Volume** to see the field distribution on a cross section, and on the T3P snapshot series to animate it.

Clip and Slice act on whatever is selected in the Pipeline Browser. Select **Entire Volume** for the field inside, **External Surface** for the walls.

## Save a movie

The quick way:

1. Arrange the view and check the animation with the VCR controls (**View, then Animation View** if the toolbar is hidden). For a T3P series the time steps are the snapshots; for a set of Omega3P modes use the `nextmode` macro.
2. **File, then Save Animation**. Choose **PNG**, one file per frame; the other formats cost disk space or image quality.
3. Set the frame size. Decide the aspect ratio first and, if you want exactly that size, lock it with **Tools, then Lock View Size Custom**.
4. Encode the PNG frames with `ffmpeg` into an H.264 `.mp4`, which plays everywhere:

```bash
ffmpeg -framerate 15 -i frame.%04d.png -c:v libx264 -pix_fmt yuv420p movie.mp4
```

The T3P and Track3P tutorials give the typical frame counts: one frame per snapshot or per saved particle time.

## Vector field as cones

1. Select **Entire Volume** (needs **Read Internal Volume**) and add **Filters, then Alphabetical, then Slice** to get a plane through the model; or skip the slice to glyph the whole volume.
2. With the slice selected, add **Glyph** (the glyph icon on the Common toolbar).
3. Set **Orientation Array** to the field (`efield` or `bfield`), **Scale Array** to the same field, and **Glyph Type** to **Cone**.
4. Under **Masking**, choose **Every Nth Point** or **Uniform Spatial Distribution** so the cones are not too dense; **All Points** draws one per mesh node.
5. **Apply**. The cones will be the wrong size; set **Scale Factor** down by an order of magnitude or so and **Apply** again until they look right.
6. For figures, make the cones thin (**Radius** about 0.2) and smooth (**Resolution** 12 to 18).

## Identify a surface ID

Sidesets from Cubit appear in ParaView as blocks numbered by surface ID. To find which surface is which:

1. Select **External Surface** in the Pipeline Browser.
2. Press **b** (or **Edit, then Select Block**) and drag a rectangle over part of the surface you want.
3. The selected surface is highlighted in magenta. Open **View, then Find Data**; the selection lists the block, and the block name carries the surface ID.
4. If you know the ID and want to see where it is: **Edit, then Find Data**, set the data producer to the reader and select by **Block ID**; or expand the multiblock in the **Multi-block Inspector** (**View, then Multi-block Inspector**) and toggle blocks on and off.

The surface ID is what `Boundary` and `Port` blocks, TEM3P `HeatSource` and Track3P `Material` blocks refer to in the input file.

## Find a node and its coordinates and field values

1. Display the mesh as **Surface** (not wireframe) and zoom in on the region of interest.
2. Press **d** (or **Edit, then Select Points On**) and drag a rectangle around the nodes.
3. To label them, open **View, then Find Data** and under **Selection Display**, turn on **Point Labels** with the ID.
4. For coordinates and field values, split the view (**Split Vertical** in the top right corner of the render view) and open a **Spreadsheet View** in the new half. Set its **Attribute** to **Point Data** and click **Show only selected elements**. Widen the vector columns to see all three components.

## Particles and trajectories

Track3P and Pic3P write particle files that the SLAC reader loads along with the mesh.

**Make the particles visible.** Switch the mesh to wireframe-front style or hide it, and step forward in time if nothing shows: in many runs there are no particles at the first step.

**Trails.** Select the particle source and add **Filters, then Alphabetical, then Temporal Particles To Pathlines**. **Mask Points** 1 keeps every particle (2 keeps every other, and so on); **Max Track Length** sets how many time steps the trail covers. **Apply** creates two outputs, **Pathlines** and **Particles**. Trails grow as you play forward one step at a time; jumping or stepping backward resets them.

**Heads as spheres.** Select the new **Particles** output and add **Glyph** with **Glyph Type** Sphere, **Scale Array** none (so every sphere is the same size), **Masking** All Points. **Apply**, then reduce **Scale Factor** until the spheres look right. Color by `EmissionType`, `Momentum`, or a solid color. Hide the original particle source so its white dots do not show on the spheres.

**Trails as tubes.** Select **Pathlines**, add **Tube**, set **Number of Sides** to 8 or more and a **Radius** about half the sphere radius. A solid light color on the tubes with momentum on the spheres is usually the clearest.

**Troubleshooting.** Spheres of wildly different sizes: Scale Array is set, clear it. Spheres all the same but too large: lower Scale Factor. Colors too uniform: **Rescale to Data Range** uses the current time step, so for multipacting step to just before an impact, when momentum is highest, and rescale there. Slow rendering during trial runs: lower the sphere and tube resolution, or temporarily color the raw points and lines instead of glyphs.

## Smoother curved surfaces

Curved elements are drawn with straight edges. Two remedies, which can be combined:

- Check **Read Midpoints** on the reader and **Apply**; the surface then uses the quadratic edge midpoints.
- Enable **Read Internal Volume**, hide **External Surface**, select **Entire Volume**, add **Extract Surface** and then **Generate Surface Normals**. Adjust **Feature Angle** if creases appear where the surface should be smooth, or vice versa.

## Export the field on a plane as CSV

To hand field data to other software on a regular grid:

1. Load mesh and mode with **Read Internal Volume** enabled; show **Entire Volume** and hide **External Surface**.
2. Select **Entire Volume** and add **Filters, then Alphabetical, then Resample To Image**. Check **Use Input Bounds** off and type **Sampling Bounds** that span the plane you want (give the thin dimension a zero extent) and **Sampling Dimensions** such as 100 x 100 x 1. **Apply**.
3. With only the resample filter visible, **File, then Save Data**, choose **CSV**. In the writer dialog leave **Write All Time Steps** off and set **Field Association** to **Points**.

For an arbitrary cut instead of an axis-aligned grid, use **Slice** and save its point data the same way; the points then follow the mesh rather than a uniform grid.

## Large data: client-server mode

For results too large for the ThinLinc desktop, run a parallel ParaView server on Perlmutter and connect the ParaView client on your computer to it. NERSC documents the setup at [docs.nersc.gov/applications/paraview](https://docs.nersc.gov/applications/paraview/); the client version must match the server version listed there.
