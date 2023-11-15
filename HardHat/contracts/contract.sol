// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;
pragma abicoder v2;


import "./standart_token/token/ERC20/ERC20.sol";
import "./standart_token/token/ERC1155/ERC1155.sol";

// для REMIX
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract Contract is ERC20, ERC1155 {

    uint public variety_nft;
    uint public amount_collection;

    address Owner = 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266;

    uint public price_profi_token = 1;


    struct User {
        address Address;
        string Name;
    }

    struct NFT {
        uint Id;
        bool Collection;
        bool Sale;
        uint Price;
    }

    struct Nft_Sell {
        uint Id;
        NFT Nft;
        address Owner;
        uint Amount_To_Sell;
    }

     struct Collection {
        uint Id;
        uint[] Nft_In_Collection;
        uint[] Amount_For_NFT;
        bool Sale;
    }

    struct Bet {
        uint Id;
        address Owner;
        uint Price;
    }

    struct Action {
        uint Id;
        uint Id_Collection;
        address Owner;
        uint Time_Start;
        uint Time_End;
        uint Min_Price;
        uint Max_Price;
        uint Index_Max_Bet;
    }


    Nft_Sell[] public nft_sell;

    Action[] public action_collection;


    mapping (address => User) user;


    mapping (uint => NFT) public nft;

    mapping (address => uint) user_amount_variety_nft;
    mapping (address => uint) user_amount_variety_collection;


    mapping (uint => Collection) collection;
    mapping (uint => address) collection_owner;


    mapping (uint => Bet[]) bet_action;


    // modifier OnlyUser()



    function Auth() public view returns(User memory) {
        return user[msg.sender];
    }


    function Get_All_Sell_NFT() public view returns(Nft_Sell[] memory) {
        return nft_sell;
    }

    function Get_All_Action() public view returns(Action[] memory) {
        return action_collection;
    }

    // function Get_One_Action(uint id) public view returns(Action memory) {
    //     return action_collection[id];
    // }

    function Get_All_Bet_To_Action(uint id_action) public view returns(Bet[] memory) {
        return bet_action[id_action];
    }



    function Get_All_User_NFT() public view returns(NFT[] memory _nft, uint[] memory amount) {
        uint ost = variety_nft - user_amount_variety_nft[msg.sender];
        NFT[] memory user_nft = new NFT[](variety_nft - ost);
        uint[] memory amount_nft = new uint[](variety_nft - ost);

        uint push;

        for (uint i = 0; i < variety_nft; i++) {
            if (ERC1155.balanceOf(msg.sender, i) > 0) {
                user_nft[push] = nft[i];
                amount_nft[push] = ERC1155.balanceOf(msg.sender, i);
                push += 1;
            } 
        }

        _nft = user_nft;
        amount = amount_nft;
    }


    function Get_All_User_Collections() public view returns(Collection[] memory _collection) {
        uint ost = amount_collection - user_amount_variety_collection[msg.sender];
        Collection[] memory user_collection = new Collection[](amount_collection - ost);
        uint push;

        for (uint i; i < amount_collection; i++) {
            if (collection_owner[i] == msg.sender) {
                user_collection[push] = collection[i];
                push += 1;
            }
        }

        _collection = user_collection;
    }


    function Get_Ballanse() public view returns(uint) {
        return ERC20.balanceOf(msg.sender);
    }


    function Get_Ether_Ballance() public view returns(uint) {
        return msg.sender.balance;
    }





    function Buy_Profi(uint amount) public payable {
        require(msg.value == amount * price_profi_token, "Invalid msg.value");
        payable(msg.sender).transfer(amount * price_profi_token);
        ERC20._transfer(Owner, msg.sender, amount);
    }







    function Set_Only_NFT(uint amount, uint price) public {
        require(amount > 0, "Invalid amount");

        ERC1155._mint(
            msg.sender, 
            variety_nft, 
            amount, 
            ""
        );

        nft[variety_nft] = NFT(
            variety_nft,
            false,
            false,
            price
        );

        user_amount_variety_nft[msg.sender] += 1;
        variety_nft += 1;
    }

    
    function Sell_NFT(uint id, uint amount) public {
        require(id < variety_nft, "Invalid id");
        require(ERC1155.balanceOf(msg.sender, id) >= amount, "Invalid amount");
        require(nft[id].Collection == false, "This token in colection");
        require(nft[id].Sale == false, "This token already sell");

        nft_sell.push(Nft_Sell(
            nft_sell.length,
            nft[id],
            msg.sender,
            amount
        ));

        nft[id].Sale = true;
    }


    function Buy_NFT(uint index, uint amount) public {
        address _owner = nft_sell[index].Owner;
        uint _price = nft[nft_sell[index].Nft.Id].Price;
        uint _id_token = nft_sell[index].Nft.Id;

        require(index < nft_sell.length, "Invalid id");
        require(nft_sell[index].Amount_To_Sell >= amount, "Invalid amount");
        require(nft[nft_sell[index].Nft.Id].Collection == false, "This token in colection");
        require(nft[nft_sell[index].Nft.Id].Sale == true, "This token not sell");
        require(ERC20.balanceOf(msg.sender) >= amount * _price, "Not money");

        if (amount == nft_sell[index].Amount_To_Sell) {
            if (index < nft_sell.length) {
                nft_sell[nft_sell.length -1].Id  = nft_sell[index].Id;
                nft_sell[index] = nft_sell[nft_sell.length -1];
            }

            nft_sell.pop();
            nft[_id_token].Sale = false;

            user_amount_variety_nft[_owner] -= 1;

        } else {
            nft_sell[index].Amount_To_Sell -= amount;
        }

        ERC20._transfer(msg.sender, _owner, amount * _price);

        ERC1155.safeTransferFrom(
                _owner, 
                msg.sender, 
                _id_token, 
                amount, 
                ""
        );

        user_amount_variety_nft[msg.sender] += 1;
    }
    
    
    function Set_Collection() public{
        collection[amount_collection] = Collection(
            amount_collection,
            new uint[](0),
            new uint[](0),
            false
        );

        collection_owner[amount_collection] = msg.sender;
        user_amount_variety_collection[msg.sender] += 1;

        amount_collection +=1;
    }


    function Set_NFT_In_Collection(uint id, uint amount) public {
        require(id <= amount_collection, "Invalid id");
        require(amount > 0, "Invalid amount");
        require(collection_owner[id] == msg.sender, "You're not Owner this collection");

        ERC1155._mint(
            msg.sender, 
            variety_nft, 
            amount, 
            ""
        );

        nft[variety_nft] = NFT(
            variety_nft,
            true,
            false,
            0
        );

        collection[id].Nft_In_Collection.push(variety_nft);
        collection[id].Amount_For_NFT.push(amount);

        user_amount_variety_nft[msg.sender] += 1;

        variety_nft += 1;
    }



    function Set_Action(
        uint id_collection, 
        uint start_time, 
        uint end_time, 
        uint min_price,
        uint max_price
    ) public {
        require(id_collection <= amount_collection, "Invalid id");
        require(collection_owner[id_collection] == msg.sender, "You're not Owner");
        require(collection[id_collection].Sale == false, "Collection is alredy sell");
        require(start_time >= block.timestamp && end_time >= block.timestamp, "Invalid time");
        require(min_price > 0 && max_price > min_price, "Invalid price");

        collection[id_collection].Sale = true;

        action_collection.push(Action(
            action_collection.length,
            id_collection,
            msg.sender,
            start_time,
            end_time,
            min_price,
            max_price,
            0
        ));
    }



    function Set_Bet_To_Action(uint id, uint bet) public {
        require(id <= action_collection.length, "Invalid id");
        require(action_collection[id].Time_Start <= block.timestamp, "Action don't start");
        require(action_collection[id].Time_End >= block.timestamp, "Action the end");
        require(ERC20.balanceOf(msg.sender) >= bet, "Invalid money");
        require(action_collection[id].Min_Price <= bet, "You're bet small start bet");
        require(action_collection[id].Max_Price >= bet, "You're bet many max bet");
        require(bet_action[id][action_collection[id].Index_Max_Bet].Price < bet, "Bet is small");

        action_collection[id].Index_Max_Bet = bet_action[id].length;

        bet_action[id].push(Bet(
            bet_action[id].length,
            msg.sender,
            bet
        ));
    }



    function End_Action(uint id) public {
        address _owner_bet = bet_action[id][action_collection[id].Index_Max_Bet].Owner;

        require(id <= action_collection.length, "Invalid id");
        require(action_collection[id].Owner == msg.sender, "You're not Owner thic Action!");
        require(action_collection[id].Time_Start < block.timestamp, "Action don't start");
        require(action_collection[id].Time_End >= block.timestamp, "Action the end");


        ERC20._transfer(
            _owner_bet, 
            msg.sender, 
            bet_action[id][action_collection[id].Index_Max_Bet].Price
        );


        ERC1155.safeBatchTransferFrom(
            msg.sender, 
            _owner_bet, 
            collection[action_collection[id].Id_Collection].Nft_In_Collection,
            collection[action_collection[id].Id_Collection].Amount_For_NFT,
            ""
        );
 
        collection[action_collection[id].Id_Collection].Sale = false;
        collection_owner[action_collection[id].Id_Collection] = _owner_bet;


        bet_action[id] = bet_action[action_collection.length -1];
        delete bet_action[action_collection.length -1];
        if (id < action_collection.length) {
            action_collection[action_collection.length -1].Id = action_collection[id].Id;
            action_collection[id] = action_collection[action_collection.length -1];
        }
        action_collection.pop();

        user_amount_variety_collection[msg.sender] -= 1;
        user_amount_variety_collection[_owner_bet] += 1;
    }







































    constructor() ERC20("Professional", "PROFI") ERC1155("uri") {
        ERC20._mint(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, 1000000);

        user[0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266] = User(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, "Gey");

        





        user[0x70997970C51812dc3A010C7d01b50e0d17dc79C8] = User(0x70997970C51812dc3A010C7d01b50e0d17dc79C8, "gdfgdfg");


        user[0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC] = User(0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC, "ouipouio");

        user[0x90F79bf6EB2c4f870365E785982E1f101E93b906] = User(0x90F79bf6EB2c4f870365E785982E1f101E93b906, "vbnvbn");


    }
}