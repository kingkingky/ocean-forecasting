
import cdsapi
import xarray as xr
import calendar
from pathlib import Path

# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(
    "/home/kankrit/Projects/ocean-forecasting/data/raw"
)

HEAT_FLUX_DIR = BASE_DIR / "era5" / "heat_flux"
TEMP_DIR = HEAT_FLUX_DIR / "temp_raw"

TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Recommended ERA5 heat budget variables
VARIABLES = {
    "surface_net_solar_radiation": "ssr",
    "surface_net_thermal_radiation": "str",
    "surface_latent_heat_flux": "slhf",
    "surface_sensible_heat_flux": "sshf",
}

DATASET = "reanalysis-era5-single-levels"

# Download all 24 hourly timestamps
HOURS = [f"{h:02d}:00" for h in range(24)]

# Start with one month for testing.
# After verifying the output, change to:
# YEARS = range(2017, 2022)
# MONTHS = range(1, 13)

YEARS = range(2017, 2022)
MONTHS = range(1, 13)

client = cdsapi.Client()


# ==========================================
# 2. DOWNLOAD AND EXTRACT
# ==========================================

for year in YEARS:

    for month in MONTHS:

        year_str = str(year)
        month_str = f"{month:02d}"

        print("\n" + "=" * 70)
        print(f"Processing {year_str}-{month_str}")
        print("=" * 70)

        # Prepare output directories
        output_paths = {}

        for short_name in VARIABLES.values():

            var_dir = HEAT_FLUX_DIR / short_name
            var_dir.mkdir(parents=True, exist_ok=True)

            output_paths[short_name] = (
                var_dir /
                f"{short_name}_{year_str}_{month_str}.nc"
            )

        # Skip if all variables already exist
        if all(p.exists() and p.stat().st_size > 0
               for p in output_paths.values()):

            print("✅ All variables already exist. Skipping.")
            continue

        # Temporary combined file
        raw_file = (
            TEMP_DIR /
            f"era5_heat_flux_{year_str}_{month_str}_raw.nc"
        )

        # ======================================
        # 2.1 DOWNLOAD
        # ======================================

        if not raw_file.exists():

            print("⬇️ Downloading ERA5 Heat Flux...")

            number_of_days = calendar.monthrange(
                year, month
            )[1]

            request = {
                "product_type": ["reanalysis"],

                "variable": list(VARIABLES.keys()),

                "year": [year_str],

                "month": [month_str],

                "day": [
                    f"{d:02d}"
                    for d in range(1, number_of_days + 1)
                ],

                "time": HOURS,

                # North, West, South, East
                "area": [35, 100, -10, 160],

                "data_format": "netcdf",

                "download_format": "unarchived",
            }

            client.retrieve(
                DATASET,
                request,
                str(raw_file)
            )

            print("✅ Download completed.")

        else:
            print("⏩ Reusing existing temporary file.")

        # ======================================
        # 2.2 EXTRACT VARIABLES
        # ======================================

        print("✂️ Extracting variables...")

        extraction_success = True

        with xr.open_dataset(raw_file) as ds:

            print("\nAvailable variables:", list(ds.data_vars))
            print("Dimensions:", dict(ds.sizes))

            for api_name, short_name in VARIABLES.items():

                out_path = output_paths[short_name]

                if out_path.exists() and out_path.stat().st_size > 0:
                    print(f"⏩ {short_name} already extracted.")
                    continue

                # Match either CDS long name or short name
                matched = [
                    name for name in ds.data_vars
                    if name.lower() in (
                        api_name.lower(),
                        short_name.lower()
                    )
                ]

                if not matched:
                    print(
                        f"❌ Cannot find {short_name}. "
                        f"Available: {list(ds.data_vars)}"
                    )
                    extraction_success = False
                    continue

                source_name = matched[0]

                da = ds[source_name]

                # Standardize variable name
                if source_name != short_name:
                    da = da.rename(short_name)

                # Save to temporary output first
                temp_output = out_path.with_name(
                    out_path.name + ".tmp"
                )

                da.to_dataset().to_netcdf(temp_output)

                temp_output.replace(out_path)

                print(
                    f"✅ {short_name} saved: "
                    f"{out_path.name}"
                )

        # ======================================
        # 2.3 CLEANUP
        # ======================================

        all_outputs_exist = all(
            p.exists() and p.stat().st_size > 0
            for p in output_paths.values()
        )

        if extraction_success and all_outputs_exist:

            raw_file.unlink(missing_ok=True)

            print("✅ Extraction completed. Raw file removed.")

        else:

            print(
                "⚠️ Some outputs are missing. "
                "Raw file retained for recovery."
            )


print("\n🎉 Heat Flux download process finished!")
