import streamlit as st
import requests
import argparse

# Get the server URL from command line arguments

st.set_page_config(
    page_title="Text-to-SQL NLP",
    layout="wide"
)

def main():
	st.title("Text-to-SQL NLP Application")
	st.write("Enter a natural language query to generate SQL code.")

	user_input = st.text_input("Natural Language Query", "Find all employees in Singapore")
	
	if st.button("Generate SQL"):
		with st.spinner("Generating SQL..."):
		# Here you would call your NLP model to generate SQL from the user input
			response = requests.post(f"{SERVER_URL}/api/v1/query", json={"question": user_input})
			error = response.json().get("error")
			if response.status_code != 200:
				st.error(f"Error from server: {response.status_code}")
				return
			if error:
				st.error("Failed to generate - \t" + error)
				st.error(response.json())
				return
			else:
				sql_query = response.json().get("sql", "-- no SQL generated")
				st.code(sql_query, language='sql')
				results = response.json().get("results", [])
				if results:
					st.write("Query Results:")
					row_count = len(results)
					st.caption(f"{row_count} rows returned")
					st.dataframe(results)
				else:
					st.info("Query ran successfully but returned no results.")

if __name__ == "__main__":
	main()
