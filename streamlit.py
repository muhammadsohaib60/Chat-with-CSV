import streamlit as st
import pandas as pd
import requests

# Streamlit app


def main():
    st.title("CSV File Uploader")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read and display the uploaded file content
        df = pd.read_csv(uploaded_file, index_col=False)
        st.write(df)

        # Save the uploaded file to data.csv
        df.to_csv("data.csv")

        # Input text
        input_text = st.text_input("Enter your question")

        # Send data to Flask
        if st.button("Ask"):
            url = "http://127.0.0.1:5001"  # Replace with your Flask endpoint
            data = {
                "input_text": input_text,
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.success("Data sent successfully!")
                print(response.text)
                st.write(response.text)
            else:
                st.error("Failed to send data")
                st.write(response.text)


if __name__ == "__main__":
    main()
