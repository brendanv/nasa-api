import argparse

from nasa import earth


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop land from SAR image.")
    parser.add_argument("--lat", required=True, type=float,
                        help="Required. Path to SAR TIFF to crop.")
    parser.add_argument("--lon", required=True, type=float,
                        help="Required. Path to land borders shapefile, specifying where to crop.")
    # parser.add_argument("--dim", default=0.025, type=float, # NOT WORKING CORRECTLY?
    #                     help="Optional. Width and height of image in degrees.")
    parser.add_argument("--date", default="None",
                        help="Optional. date of image (YYYY-MM-DD); if not supplied, then the most recent image (i.e., closest to today) is returned.")
    parser.add_argument("--cloud", default=True, action='store_true',
                        help="Optional. Calculate the percentage of the image covered by clouds.")
    parser.add_argument("--out_path", default="/tmp/image.png",
                        help="Optional. Where to save output.")
    args = parser.parse_args()

    image_response = earth.image(lat=args.lat, lon=args.lon, dim=None, date=args.date, cloud_score=args.cloud)

    print "Image Date/Time: {}.".format(image_response.date)
    print "The percentage of the image covered by clouds was calculated as {}.".format(image_response.cloud_score)
    image_response.image.save(args.out_path)
