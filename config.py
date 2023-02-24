import json
from web3 import Web3

BOT_TOKEN = "5959869028:AAEoH0A3LsFUryD83MOMCobQOQ5TFRdAu4w"
CATEGORIES = ["Business", "Crypto", "Finance", "Sports", "Media", "Influencer", "Actor", "Baking", "Cooking", "Nature", "DIY", "Celebrity"]
RPC_ADDRESS = "https://rpc.ankr.com/bsc_testnet_chapel"
PAYMENT_CONTRACT = Web3.toChecksumAddress("0xF300883543a62fe08e2bD1AaABAEe2dAd3Aa3d19") #Web3.toChecksumAddress("0x3fba9c7f943068064de77394016dc0995ddea228")
TTN_CONTRACT = Web3.toChecksumAddress("0xbf0Ce765F58E12a9Dd0cD778047530E5Db4AcAb5")
BUSD_CONTRACT = Web3.toChecksumAddress("0xdF0B1A40ec08818B7ac2Af1514C16B023939Ee43")
PAYMENT_CONTRACT_ABI = json.loads("""
[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_staking_fees",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_dev_fees",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "group_owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "order_id",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "acceptedPaymentBNB",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "group_owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "order_id",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "token_contract",
				"type": "address"
			}
		],
		"name": "acceptedPaymentToken",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "group_owner",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "order_id",
				"type": "string"
			}
		],
		"name": "acceptPaymentBNB",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "recipient_",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount_",
				"type": "uint256"
			}
		],
		"name": "acceptPaymentBUSD",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "recipient_",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount_",
				"type": "uint256"
			}
		],
		"name": "acceptPaymentTTN",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	},
	{
		"inputs": [],
		"name": "busd_contract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "buy_back_contract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "dev_fees",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "project_wallet",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "staking_fees",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "staking_pool_address",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "token_contract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
""")
TTN_CONTRACT_ABI = json.loads("""
[{"inputs":[{"internalType":"address","name":"routerAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[],"name":"FeesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldRouter","type":"address"},{"indexed":false,"internalType":"address","name":"newRouter","type":"address"}],"name":"UpdatedRouter","type":"event"},{"inputs":[],"name":"BUSD","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"name":"airdropTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"allowedTransfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"bool","name":"state","type":"bool"}],"name":"bulkExcludeFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"buytaxes","outputs":[{"internalType":"uint256","name":"reward","type":"uint256"},{"internalType":"uint256","name":"marketing","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"project","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"devWallet","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"disableTransferTax","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enableTransferTax","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"marketingWallet","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxBuyLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSellLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxWalletLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferRfi","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddr","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"rescueAnyBEP20Tokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"busdAmount","type":"uint256"}],"name":"rescueBUSD","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"router","outputs":[{"internalType":"contract IRouter","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sellTaxes","outputs":[{"internalType":"uint256","name":"reward","type":"uint256"},{"internalType":"uint256","name":"marketing","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"project","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_reward","type":"uint256"},{"internalType":"uint256","name":"_marketing","type":"uint256"},{"internalType":"uint256","name":"_liquidity","type":"uint256"},{"internalType":"uint256","name":"_project","type":"uint256"}],"name":"setBuyTaxes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_reward","type":"uint256"},{"internalType":"uint256","name":"_marketing","type":"uint256"},{"internalType":"uint256","name":"_liquidity","type":"uint256"},{"internalType":"uint256","name":"_project","type":"uint256"}],"name":"setSellTaxes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"state","type":"bool"}],"name":"setTradingStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"swapTokensAtAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totFeesPaid","outputs":[{"internalType":"uint256","name":"reward","type":"uint256"},{"internalType":"uint256","name":"marketing","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"project","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tradingEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferTaxEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bool","name":"state","type":"bool"}],"name":"updateAllowedTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newWallet","type":"address"}],"name":"updateMarketingWallet","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxBuy","type":"uint256"},{"internalType":"uint256","name":"maxSell","type":"uint256"}],"name":"updateMaxTxLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"updateMaxWalletlimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newWallet","type":"address"}],"name":"updateProjectWallet","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newRouter","type":"address"},{"internalType":"address","name":"newPair","type":"address"}],"name":"updateRouterAndPair","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"updateSwapEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"updateSwapTokensAtAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
""")
