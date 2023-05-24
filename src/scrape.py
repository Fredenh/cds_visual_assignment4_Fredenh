import argparse
import json
import os
import requests

def parse_arguments():
    # Defining command line argument parser
    parser = argparse.ArgumentParser()
    # Adding --query argument with default value and help message. This is for the sake of scraping every of the 5 sports at ones own will
    parser.add_argument('--query', type=str, default='padel tennis',
                        help='Search query for Pexels')
    # Parsing the command line arguments and returning the parsed query
    args = parser.parse_args()
    return args.query

def main():
    # Parsing the query from command line arguments
    query = parse_arguments()

    # Setting up the search parameters for the images
    per_page = 80  # A set maximum value for per_page is 80
    total_images = 240 # Total amount of images scraped before stopping
    # My personal API key 
    api_key = "Wp6anIfOgkxac7KFJN8AbUvRGRBA7czoWx6yNhByNuRykla6XPTvPkZc"  

    # This dictionary shows which preset queries to use to get the exact same data as me. 
    query_to_folder = {
        "badminton play": "badminton",
        "padel tennis": "padel",
        "squash sport": "squash",
        "table tennis": "table_tennis",
        "tennis sport": "tennis"
    }

    # Getting the output folder based on the search query
    out_folder = query_to_folder.get(query, "other") # the "other" refers to if an argument is added in the command line that does not correspond to the preset queries above. The line simply makes a new folder called "out", and places the scraped images there.

    # Specifying the output folder path
    outpath = os.path.join(".", "in", out_folder)
    os.makedirs(outpath, exist_ok=True)

    # Calculating the number of pages needed to reach 240 images
    num_pages = (total_images + per_page - 1) // per_page

    # Initializing the image count
    image_count = 0

    # For loop making API requests for each page
    for page in range(1, num_pages + 1):
        # Constructing the API request URL with the query, per_page, and page which were defined before
        url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}"
        # Setting the headers with the API key
        headers = {"Authorization": api_key}
        # Sending the GET request to the Pexels API
        response = requests.get(url, headers=headers)
        # Parsing the JSON response
        data = json.loads(response.text)

        # Processing the API response and extracting image URLs
        # Making empty list for later appending
        image_urls = []
        for photo in data['photos']:
            image_urls.append(photo['src']['original'])

        # Downloading images
        for i, image_url in enumerate(image_urls):
            # This if statement checks if the desired number of images has been reached. If it has, then it stops
            if image_count >= total_images:
                break

            # Sending a GET request to download the image
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                # Making complete image path with f string to create a nicely indexed list of images in the folder
                image_path = os.path.join(outpath, f"image_{image_count + 1}.jpg")
                # Saving the image file by "writing" it as a txt
                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                # Printing success message for each successfully downloaded image
                print(f"Image {image_count + 1} downloaded successfully.")
            else:
                # Printing failure message 
                print(f"Failed to download Image {image_count + 1}.")

            # Keeping track of the image count
            image_count += 1

if __name__ == '__main__':
    main()
