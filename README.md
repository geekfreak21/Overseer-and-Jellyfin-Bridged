# Overseer-Jellyfin Bridge Script

This repository hosts a Python script designed to enhance the streaming experience for Jellyfin users by integrating with Overseer. Inspired by Plex's direct download feature from watchlists, this script automates the process of listing TV shows from any streaming provider, creating placeholders within Jellyfin and facilitating seamless downloads directly from your favorites list.

## Features

- **Automated Show Listing**: Automatically lists TV shows from various streaming services (Netflix, Hulu, HBO, Prime Video, Disney, etc.) within Jellyfin as placeholders.
- **Easy Downloads**: Sends download requests to Overseer when you mark a show as a favorite.
- **Customizable**: Allows selection of streaming service shows to fetch and display in Jellyfin.

## Getting Started

### Prerequisites

- Jellyfin media server setup
- Overseer for managing media requests
- UserScripts plugin installed in Unraid (if applicable)
- Familiarity with your Jellyfin media directory structure

### How-To

1. **Create Service Folders**: Manually create folders named after each streaming service (e.g., Netflix, Hulu) in your Jellyfin media directory.

    ![Service Folders](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/687d895f-ef57-466f-9d81-84a2aa2ecc40)

2. **Modify Showv2.py**:

    ![Modify Showv2.py](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/1ade1266-5269-4fe0-9823-3292f32d1398)

    For the network ID from Overseer, navigate to a streaming service within Overseer:

    ![Streaming Service](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/72338688-654e-463b-84dd-908b9ddc6bb5)

    Select a streaming service:

    ![Select Service](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/dca3f06f-f550-4a09-acc2-ada9a7594427)

    The URL will show something like `https://ipaddress/discover/tv/network/213` - `213` is your network ID.

    Don't forget to modify the `shows_dir`, `overserr_url`, `service_directories`, and add your Overseer API key in `X-API-Key`:

    ![API Key](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/7372c905-b25c-489f-99fe-7da1b8e86b10)

3. **Modify Webv2.py**:

    Ensure your Overseer account is local for this to work. Modify `shows_dir` to the path where your movies and TV shows are downloaded.

4. **Run the Scripts** in Unraid through the UserScripts plugin:

    For `showsv2.py`:

    ![Showsv2.py](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/bff8a9ca-f831-485e-9498-8de3292acc8c)

    For `webv2.py`:

    ![Webv2.py](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/6d813b5c-6371-401b-8d7f-c209746b5518)

    Set `showsv2.py` to run daily and `webv2.py` to run at Unraid startup.

5. **Optional**: Create a library in Jellyfin named after the streaming service of your choice and set the path to the corresponding service folder you created.

    ![Library Setup](https://github.com/geekfreak21/Overseer-and-Jellyfin-Bridged/assets/102196550/322b0714-bf7a-44b5-9279-83ff18ec62fd)

6. **Scan Jellyfin Library**: Scan your Jellyfin library to see the newly populated shows from your chosen streaming services.

### Usage

Mark any show as a favorite in Jellyfin to automatically send a download request to Overseer. The script monitors these favorite requests and communicates with Overseer to manage the download process.

## Contributing

We're looking forward to developing this script into a fully-fledged Jellyfin plugin and welcome any contributions! Whether you're interested in coding, documentation, or testing, your help would be greatly appreciated.
