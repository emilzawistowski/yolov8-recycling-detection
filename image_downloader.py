from bing_image_downloader import downloader
import os


def download_images():
    queries = [
        "chair",
        "couch",
        "bed",
        "dining table",
        "bench"
    ]

    limit_images = 50
    output_dir = 'dataset'

    print(f"Start of downloading {limit_images} images for every {len(queries)} categories...")
    print("-" * 40)

    for query in queries:
        print(f"--> Downloading for: {query}")

        try:
            downloader.download(
                query,
                limit=limit_images,
                output_dir=output_dir,
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
                verbose=False
            )
            print(f"    [OK] Finished for: {query}")
        except Exception as e:
            print(f"    [BŁĄD] Problem for {query}: {e}")

    print("-" * 40)
    print(f"Ready: '{os.path.abspath(output_dir)}'")


if __name__ == "__main__":
    download_images()