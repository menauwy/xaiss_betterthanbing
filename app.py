# key packages
from cProfile import label
import streamlit as st
from reranker import search_intent

base_url = "https://better.than.bing.com/ask.json?description={}"
index_path = '/home/wang/xaiss/datasets/scidocs/corpus_index'
#query = 'what is explainable AI'


# retrieve data
#def get_data(search):
    #resp = requests.get(url)
    #resp= [{"id": "11111", "contents": "This is the contents...."}, 
    #        {"id": "22222", "contents": "This is the contents...."},
    #        {"id": "33333", "contents": "This is the contents...."}]
    #return resp.json
#    return




RESULT_TEMP = """
<div style="border-style: solid;">
    <h5>{}</h5>
    <p>{}</p>
</div>
"""

def main():
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.title("BetterThanBing")

    if choice == "Home":
        st.subheader("Home")

        # search form
        with st.form(key="searchform"):
            nav1, nav2 = st.columns([3, 1])

            with nav1:
                search_term = st.text_input("Wanna search something?")
            with nav2:
                #st.text("Go for it..")
                submit_search = st.form_submit_button(label='Search')

        st.success("You searched for '{}'.".format(search_term))


        # intent results
        col1, col2 = st.columns([3, 3])

        with col1:
            if submit_search:
                search_url = base_url.format(search_term)

                #st.write(search_url)

                #data = get_data(search_url)
                expansion, top_doc = search_intent(index_path, search_term)
                num_of_results = len(top_doc)
                topk = 10
                st.subheader("Showing the top {} results. {} results found in total".format(topk, num_of_results))
                #st.write(data)

                st.write(expansion)

                for d in top_doc:
                    result_id = d['id']
                    result_co = d['contents']
                    st.markdown(RESULT_TEMP.format(result_id, result_co), unsafe_allow_html=True)
        
        with col2:
            if submit_search:
                search_url = base_url.format(search_term)

                #st.write(search_url)

                #data = get_data(search_url)
                expansion, top_doc = search_intent(index_path, search_term)
                num_of_results = len(top_doc)
                topk = 10
                st.subheader("Showing the top {} results. {} results found in total".format(topk, num_of_results))
                #st.write(data)

                st.write(expansion)

                for d in top_doc:
                    result_id = d['id']
                    result_co = d['contents']
                    st.markdown(RESULT_TEMP.format(result_id, result_co), unsafe_allow_html=True)



        # document representation

    else:
        st.subheader("About")
        




if __name__ == "__main__":
    main()
