# Rifas Module for Odoo 18.0

## Overview
The **Rifas** module is designed to manage raffles efficiently within Odoo 18.0. It provides tools to create, manage, and track raffles, participants, and winners, streamlining the process for businesses or organizations.

## Features
- Create and configure raffles with customizable settings.
- Manage participants and their tickets.
- Automatic winner selection based on randomization.
- Track raffle history and results.
- Integration with Odoo's reporting and notification systems.

## Installation
1. Clone or download the module into your Odoo addons directory:
    ```bash
    git clone <repository_url> /c:/projectos/odoo/data_dir/addons/18.0/rifas
    ```
2. Restart your Odoo server:
    ```bash
    ./odoo-bin -c <config_file>
    ```
3. Activate the developer mode in Odoo.
4. Go to **Apps**, search for "Rifas," and install the module.

## Usage
1. Navigate to the **Rifas** menu in your Odoo dashboard.
2. Create a new raffle by clicking on **Create** and filling in the required details.
3. Add participants and assign tickets.
4. Use the **Draw Winner** button to randomly select a winner.
5. View raffle results and export reports as needed.

## Configuration
- Access the **Settings** menu under the Rifas module to configure default values for raffles.
- Set up email templates for notifying participants and winners.

## Dependencies
This module depends on the following Odoo core modules:
- `base`
- `mail`

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License
This module is licensed under the MIT License. See the `LICENSE` file for more details.

## Changelog
### Version 1.0.0
- Initial release of the Rifas module.
- Core functionality for managing raffles and participants.
- Winner selection and reporting features implemented.
- Basic configuration options added.