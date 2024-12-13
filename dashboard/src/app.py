import streamlit as st


def main():
    st.title("IX | 70126 | IOT Consumer Value Dashboard")
    st.navigation(
        {
            "Analysis Platform": [
                st.Page("./views/home.py", title="Home Page", icon="🏠"),
                st.Page(
                    "./views/data_insights.py", title="Additional Analysis", icon="🔍"
                ),
            ],
            "Data Explorer": [
                st.Page(
                    "./views/mined_data.py",
                    title="Mined Data Collections Viewer",
                    icon="⛏️",
                ),
                st.Page(
                    "./views/api_data.py", title="API Data Collection Viewer", icon="🛂"
                ),
            ],
        }
    ).run()


if __name__ == "__main__":
    main()
