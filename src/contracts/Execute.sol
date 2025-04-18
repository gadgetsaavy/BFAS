// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v3-core/contracts/interfaces/IUniswapV3Pool.sol";
import "@uniswap/v3-periphery/contracts/interfaces/INonfungiblePositionManager.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";

contract Execute {
    ISwapRouter public swapRouter;
    address public owner;

    // Token addresses (WETH, DAI, USDT, etc.)
    address private WETH;
    address private DAI;
    address private USDT;
    address private MATIC;
    address private TETHER;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor(address _swapRouter) {
        swapRouter = ISwapRouter(_swapRouter);
        owner = msg.sender;
    }

    // Function to execute arbitrage
    function executeArbitrage(address[] calldata path, uint256 amountIn) external onlyOwner {
        // Ensure path is valid
        require(path.length >= 2, "Invalid path");

        uint256 amountOutMin = 0; // We won't perform a slippage check here as per your requirement
        uint256 amountOut;

        for (uint256 i = 0; i < path.length - 1; i++) {
            // Execute the swap from token[i] to token[i+1]
            uint256 amountIn = IERC20(path[i]).balanceOf(address(this));
            IERC20(path[i]).approve(address(swapRouter), amountIn);

            ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
                tokenIn: path[i],
                tokenOut: path[i + 1],
                fee: 3000, // Using the 0.3% fee tier for Uniswap V3
                recipient: address(this),
                deadline: block.timestamp + 300,
                amountIn: amountIn,
                amountOutMinimum: amountOutMin,
                sqrtPriceLimitX96: 0
            });

            amountOut = swapRouter.exactInputSingle(params);
        }

        // Logic to handle flash loan repayment and profit distribution
        uint256 profit = amountOut - amountIn;
        payable(owner).transfer(profit);
    }

    // Function to deposit tokens into the contract
    function depositTokens(address token, uint256 amount) external {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }
}
