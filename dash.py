import streamlit as st
from pdf2image import convert_from_path
import os
from PIL import Image
from main import predict

st.title("TableNet with OCR Detection")
st.markdown("Hello There")

method = st.selectbox("Image or PDF", ['PDF', 'Image'])
if method == "PDF":
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
    if uploaded_file is not None:
        with open("selected.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        for _ in os.listdir("extracted_images"):
            os.remove(os.path.join("extracted_images", _))

        images = convert_from_path("selected.pdf")
        for i in range(len(images)):
            images[i].save('extracted_images/page'+'_'+ str(i+1) +'.jpg', 'JPEG')

        img_cols = st.beta_columns(len(images))
        for i in range(len(img_cols)):
            img_cols[i].subheader("page"+str(i+1))
            img_cols[i].image(Image.open("extracted_images/page_"+str(i+1)+".jpg"), use_column_width=True)

        selected_page = st.selectbox("Select the page", os.listdir("extracted_images"))

        image = Image.open('extracted_images/'+selected_page)
        st.image(image)
        
        


if method == "Image":
    st.write(method)
    uploaded_file = st.file_uploader("Choose an Image", type=['jpg','jpeg','png','bmp'])
    if uploaded_file is not None:
        with open("selected_img.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(Image.open('selected_img.jpg'), width=200)
        out = predict('selected_img.jpg', 'best_model.ckpt')
        for i in range(len(out)):
            st.dataframe(out[i])