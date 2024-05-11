import streamlit as st
import scrape_clean as sc
import analyze
import seaborn as sns
import matplotlib.pyplot as plt
st.header("Sentimental Analyzer for YT Comments")
vdo_url = st.text_input("Paste URL from Youtube")


ok = st.button("Analysis")
 
if ok:
   
    sc.main(vdo_url)
    
    sentiment_counts_test= analyze.analyze_main()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Sentiment', y='Count', data=sentiment_counts_test, palette='viridis')
    plt.title('Sentiment Analysis (Test Set)')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    st.pyplot(plt)
        
   
    
    if sentiment_counts_test['Count'][0] >  sentiment_counts_test['Count'][1]:
        
        if sentiment_counts_test['Count'][0] > sentiment_counts_test['Count'][2]: 
            st.markdown('<h3><span style="color:green;">Positively accepted the News</span></h3>', unsafe_allow_html=True)
    elif sentiment_counts_test['Count'][1] > sentiment_counts_test['Count'][2]:
        st.markdown('<h3><span style="color:red;">Negatively accepted the News</span></h3>', unsafe_allow_html=True) 
    else:
        st.markdown('<h3><span style="color:yellow;">Neutral(no effects)</span></h3>', unsafe_allow_html=True) 