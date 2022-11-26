import streamlit as st
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from PIL import Image
from io import BytesIO
from typing import List
import matplotlib
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

st.set_page_config(page_title="Gen Color List",
                   page_icon="🎨",
                   layout="wide")
col1, col2 = st.columns([3, 5])


def plot_colortable(colors, emptycols=0):
    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    names = colors

    n = len(names)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin / width, margin / height,
                        (width - margin) / width, (height - margin) / height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y - 9), width=swatch_width,
                      height=18, facecolor=name, edgecolor='0.7')
        )

    return fig


# def color_list2html(color_list: List[str]) -> str:
#     color_str = ',<br>'.join([f"""<a style="color:{i};">'{i}'</a>""" for i in color_list])
#     res = f"""<body>[{color_str}]</body>"""
#     return res
def color_list2html(color_list: List[str], justtext=True) -> str:
    if justtext:
        colorlist = [f"'{i}'" for i in color_list]
        res = ", ".join(colorlist)
        res = f"[{res}]"
        return res

    else:
        color_str = ',<br>'.join([f"""<a style="color:{i};size:4">'{i}'</a>""" for i in color_list])
        res = f"""<body style="border-style:dotted;border-width:3px;background-color:#52E396">[{color_str}]</body>"""
        return res


def image2color_list(imagedata, n_clutser):
    image_data_ = imagedata  # np.random.randint(0, 255, (300, 400, 3))
    model_data = np.concatenate([image_data_[:, :, i].reshape(-1, 1) for i in range(image_data_.shape[2])], axis=1)
    # model_data.shape
    klmodel = KMeans(n_clusters=n_clutser)
    klmodel.fit(model_data)
    color_result = [matplotlib.colors.to_hex(model_data[klmodel.labels_ == i].mean(axis=0) / 255) for i in
                    list(set(klmodel.labels_))]
    return color_result


with col1:
    with st.expander(label="⚙️Op", expanded=True):
        select_image_value = st.file_uploader(
            label="select an image",
            type=['png', 'jpg', 'jpeg'])
        select_num_cluster = st.slider(label='the number of color_palette', min_value=2, max_value=20)
        form = st.form("template_form")

        submit = form.form_submit_button("Generate Color Palette")

with col2:
    with st.expander(label="🏞️show Image", expanded=True):

        if select_image_value is not None:
            st.image(select_image_value.getvalue(),
                     # width=600,
                     caption="show image")
        else:
            st.markdown("⬅️⬅️⬅️⬅️⬅️")

    with st.expander(label="🍎show result", expanded=True):
        if submit:
            image_data_ = Image.open(BytesIO(select_image_value.getvalue())).convert('RGB')
            image_data_ = np.array(image_data_)
            # get color list

            with st.spinner('Processing...'):
                random_color = image2color_list(imagedata=image_data_, n_clutser=select_num_cluster)

            # with st.expander(label="3. show color palette", expanded=True):
            # st.markdown("## 🎨show color palette")
            fig = plot_colortable(colors=random_color)
            st.pyplot(fig)

            # with st.expander(label="🗒️color it!", expanded=True):
            # st.markdown("## 🎨copy it!")
            # st.markdown(color_list2html(random_color), unsafe_allow_html=True)
            st.text_input(label='🎨copy it!', value=color_list2html(random_color))
            st.success("success generate a color-palette from your image~")
            st.balloons()
