# Shopify Developer Challenge: Sell Your NFTS
## Written by Rohith Yenumula
This demo uses sqlite3 and flask to display a couple NFTs you've decided to add to the market. As the owner, you have the ability to sell an NFT, delete an NFT entirely, add a discount of either 10% or 50% to the price of the NFT, change the price of an NFT via an input box, or change the quantity of an NFT via an input box, all with a click of a button. 

## Usage
In order to run this application, go to the directory that contains main.py, and run

```
python3 main.py
```
Finally, go to localhost:5000 in a web browser to access the application

## Additional Features
A couple features I've thought to implement include access control, where I could disable the option to sell a certain NFT if the user is not the owner of the NFT, a user form to add an NFT to the table (which would simply be an extension of the request functionality implemented in the edit price and edit quantity features), and a real time graph of the NFT's price history, dictated by the discounts and price changes you've made to it in the past.

# NFT-image-repository
