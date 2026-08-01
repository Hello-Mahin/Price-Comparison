
import serpapi
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

api_key_val= st.secrets["api_key"]
#Function to compare the product prices
def compare(prd_name):
    client = serpapi.Client(api_key_val)
    results = client.search({
        "engine": "google_shopping",
        "q": prd_name,
        "location": "India",
        "gl": "in"
    })
    shopping_results = results["shopping_results"]
    return shopping_results



st.sidebar.title("Enter name of Product")
prd_name = st.sidebar.text_input("Enter Product Name")
number=st.sidebar.number_input("Enter Number of options here",min_value=1,max_value=20,step=1)
prd_name=prd_name.strip()
prd_name=prd_name.replace(" ","")

#main section
c1,c2= st.columns(2)
c1.image("pic.jpeg",width=300)
c2.header("Price Comparison System")

prd_comp=[]
prd_price=[]


#results section

if prd_name is not None and number is not None:
    if st.sidebar.button(" Show Compare"):
        shopping_results = compare(prd_name)
        low_price = float (shopping_results[0].get("price")[1:].replace(",",""))
        low_price_index = 0

        for _ in range(min(number,len(shopping_results))):
                current_price = float(shopping_results[_].get("price")[1:].replace(",",""))

                prd_comp.append(shopping_results[_].get("source"))
                prd_price.append(float(shopping_results[_].get("price")[1:].replace(",","")))

                st.title(f"Option {_+1}")
                c1,c2=st.columns(2)

                c1.write("Company")
                c2.write(shopping_results[_].get("title"))

                c1.write("Price")
                c2.write(shopping_results[_].get("price"))

                c1.write("Source")
                c2.write(shopping_results[_].get("source"))

                c1.write("Rating")
                c2.write(shopping_results[_].get("rating"))

                c1.write("Buy")
                c2.write("[Buy Now](%s)" % shopping_results[_].get("product_link"))

                c1.write("Thumbnail")
                c2.image(shopping_results[_].get("thumbnail"),width=85)


                st.write("---------------------------------------")

                if (current_price < low_price):
                    low_price = current_price
                    low_price_index = _

        st.sidebar.write("--------------------------------")
        st.sidebar.title("Cheapest Option : ")
        st.sidebar.image(shopping_results[low_price_index].get("thumbnail"),width=200)
        st.sidebar.write(f"Cheapest Price :{shopping_results[low_price_index].get("price")}")
        st.sidebar.write("[Buy Link](%s)" % shopping_results[low_price_index].get("product_link"))
       # st.title("Comparison System")

        st.title("Lowest Price")

        c1,c2=st.columns(2)



        c1.write("Company")
        c2.write(shopping_results[low_price_index].get("title"))

        c1.write("Price")
        c2.write(shopping_results[low_price_index].get("price"))

        c1.write("Source")
        c2.write(shopping_results[low_price_index].get("source"))

        c1.write("Rating")
        c2.write(shopping_results[low_price_index].get("rating"))

        c1.write("Buy")
        c2.write("[Buy Now](%s)" % shopping_results[low_price_index].get("product_link"))

        c1.write("Thumbnail")
        c2.image(shopping_results[low_price_index].get("thumbnail"),width=85)

        #dataframe generation for graph

        df=pd.DataFrame({
            "Product" : prd_comp,
            "Price" : prd_price
        })
        st.title("Graphical Representation of Price Comparison")
        s1,s2=st.columns(2)
        s1.bar_chart(df,x="Product",y="Price")

        s2.line_chart(df,x="Product",y="Price")

        fig,ax=plt.subplots(figsize=(10,6))
        ax.pie(df["Price"],labels=df["Product"],autopct="%1.1f%%")
        st.pyplot(fig)




