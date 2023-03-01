from web3 import Web3
from bip44 import Wallet
import streamlit as st
from web3.gas_strategies.time_based import medium_gas_price_strategy

st.set_page_config(layout="wide")
st.title("Python, Ganache and Crypto transactions using a private key") 
st.write("By Dr Yan, v1.0, 3/1/2023")

a1=" Launch Ganache first, you can download it at https://www.trufflesuite.com/ganache."
a2=" The private key depends on who is the sender (0 is the first one). "
a3=" After refreshing, you can check the sender and receiver's balances."
#

with st.expander("Click here to see (or hide) a simple explanation:"):
    st.write(a1)
    st.write(a2)
    st.write(a3)

server='HTTP://127.0.0.1:7545'
#w3 = Web3.HTTPProvider('HTTP://127.0.0.1:7545')
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545')) 


t=w3.isConnected()                 # below copy the first private key

    # HTTP://127.0.0.1:7545
col1, col2,col3 =st.columns([1,1,0.5])
col1.write(" ######   Step 1: launch Ganache")
if t==False:
    col1.write('Status: you are not connected with Ganache. Please launch Ganache and refresh your screen.')
    col1.write('If Ganache is not preinstalled, download it at https://www.trufflesuite.com/ganache.')


a=col1.text_input('Step 2 (optional): enter the server name of your Ganache, the default value is HTTP://127.0.0.1:7545')

with col1.expander("Step 3 (optional): click here to see if connected with Ganache"):
    st.write("Connected? ",t)

if t==True:
    allAccounts=w3.eth.accounts        # get all accounts
    if len(a)>0:
        w3 = Web3(Web3.HTTPProvider(a))   
    with col1.expander("Step 4 (optional): click here to show all the accounts"):
        st.write(allAccounts)
        #print(allAccounts)                 # should match 10 accounts from your Ganache 
    
    a=col1.selectbox('Step 5: choose the sender (0, 1,  ...,  9):', (0,1,2,3,4,5,6,7,8,9))
    sender    =allAccounts[a]          # the first one
    b=col1.selectbox('Step 6: choose the reseiver (0, 1, ... , 9)?', (1,2,3,4,5,6,7,8,9))
    receiver   =allAccounts[b]          # the first one

    with col1.expander("Step 7 (optional): check the balance of the sender:"):
        a=w3.eth.getBalance(sender)
        st.write(a)
    with col1.expander("Step 8 (optional): check the balance of the receiver:"):
        b=w3.eth.getBalance(receiver)
        st.write(b)
    private=col2.text_input('Step 9: Based on Step 5, copy the private key of the sender from Ganache, then paste it below')
    if col2.button("Step 10 (optional): click here to view the private key:"):    
        col2.write(private)

    if len(private)==64:
        account=w3.eth.account.from_key(private)
    
    amount = col2.number_input('Step 11: how much do you want to transfer?')
    u=col2.selectbox('Step 12: choose the unit of the above amount (ether,Gwei, or wei):', ("ether","Gwei","wei"))
    value = w3.toWei(amount, u)  # ETH 
   
    with col2.expander("Step 13 (optional): show the gas amount"):    
        w3.eth.setGasPriceStrategy(medium_gas_price_strategy) # gas price strategy 
        gasEstimate = w3.eth.estimateGas({"to":receiver,"from":sender,"value":value})
        st.write(gasEstimate)


    if col2.button("Step 14: click here to execute the transaction"):
        if len(private)==64:
            raw_tx = {"to": receiver,"from": sender, "value": value,"gas": gasEstimate, "gasPrice": 0,
              "nonce": w3.eth.getTransactionCount(sender)}
            signed_tx = account.signTransaction(raw_tx)
        if sender==account.address:
            w3.eth.sendRawTransaction(signed_tx.rawTransaction) 
            col2.write('Done!')
            st.write('From the sender of:',sender)
            st.write('To the reseivre of:',receiver)
            st.balloons()
        else:
            st.write('Error message: private key is not from the sender, check Step 6A.')
    else:
        col2.write("Error message: for Step 9, enter the private key of the sender defined by Step 5.")
else:
    st.write('')
   
#
