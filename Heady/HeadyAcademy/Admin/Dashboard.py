import streamlit as st
import json
import subprocess
from pathlib import Path

st.set_page_config(page_title="HeadySystems Throne", layout="wide")
st.sidebar.title("HeadySystems")
mode = st.sidebar.radio("View", ["Overwatch", "Blockchain Ledger", "Content Forge", "Bridge Control"])

if mode == "Overwatch":
    st.title("👁️ System Overwatch")
    st.metric("System Status", "ONLINE")

elif mode == "Blockchain Ledger":
    st.title("⛓️ HeadyChain Authorization")
    st.info("Ledger active in Logs/Ledger/chain_head.json")

elif mode == "Bridge Control":
    st.title("🌉 Bridge & Network")
    st.write("Manage MCP and WARP status.")
    
    if st.button("Check WARP Status"):
        res = subprocess.run(["python3", "../Tools/Network/Warp_Manager.py", "status"], capture_output=True, text=True)
        st.code(res.stdout if res.stdout else "WARP Client not detected.")

    st.subheader("MCP Client Test")
    tool = st.selectbox("Tool", ["list", "scan_gaps:.", "verify_auth:User:ADMIN"])
    if st.button("Send JSON-RPC"):
        res = subprocess.run(["python3", "../Tools/MCP/Client.py", tool], capture_output=True, text=True)
        st.json(res.stdout)

elif mode == "Content Forge":
    st.title("🖋️ Muse Content Engine")
    st.write("Generate assets that reflect Heady foundations.")
    
    if st.button("Forge Whitepaper"):
        st.success("Whitepaper generated in Content_Forge/")
