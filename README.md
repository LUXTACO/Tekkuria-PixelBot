# Tekkuria-PixelBot
Tekkuria is a simple yet highly customizable pixel-based aimbot designed to assist your aim efficiently. With its sleek and intuitive graphical user interface (GUI), Tekkuria stands out for its ease of use and aesthetic appeal.

## Key Features:

- **Highly Customizable**: Fine-tune Tekkuria's behavior to match your playstyle and in-game environment for unmatched precision.
- **Intuitive GUI**: The sleek and user-friendly interface makes Tekkuria easy to set up and use, eliminating frustration common with complex aimbots.
- **Enhanced Aiming**: Assist your aim efficiently with Tekkuria's pixel-based approach.

## Usage
To use Tekkuria, follow these steps:

### From source
1. **Setting Up the Environment:**
   - Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
   - Install the required Python packages by running the following command in your terminal:
     ```sh
     pip install -r requirements.txt
     ```

2. **Configuring the Bot:**
   - Navigate to the `configs` directory in the project folder.
   - You can modify existing configuration files (e.g., `aimlabs.json`, `arsenal.json`, `badbusiness.json`) or create a new JSON configuration file for your specific needs. Refer to the structure in [`configs/config.json`](configs/config.json) as a template.
   - Configuration parameters include `targetfps`, `togglekey`, `holdkey`, and visual settings like `drawbox`, `boxsettings`, etc.
   - You can also modify them by using the GUI

3. **Running the Bot:**
   - Open a terminal or command prompt in the project directory.
   - Execute the bot by running:
     ```sh
     python main.py
     ```
   - The bot will start and use the configuration specified in `configs/config.json` by default. To use a different configuration file, modify the `main.py` to load your custom config file.

4. **Compiling to Executable (Optional):**
   - If you wish to compile the bot into a standalone executable, use the provided `start_compile_nuitka.cmd` script. This requires [Nuitka](https://nuitka.net/) to be installed.
   - Run the script by double-clicking on it or executing it from the command line:
     ```cmd
     start_compile_nuitka.cmd
     ```
   - The compiled executable will be located in the `output` directory.

### From precompiled binary
1. **Download the binary from the [`Releases`](https://github.com/LUXTACO/Tekkuria-PixelBot/releases) tab**
   - Make sure to not modify the folders included in the zip
    
3. **Double click the binary and enjoy!**
   - Included binary is for windows only
     
## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.

---
<p align="center" >
  <b> >>> JOIN THE DISCORD <<< </b>
    <br>
  https://discord.gg/PdeTUZ3M62
</p>
