
# 🚗 FiveM Car Pack Organizer

A lightweight Python tool for organizing individual FiveM vehicle folders into a centralized, clean **car pack** structure for easier deployment on a FiveM server.

## 📦 What It Does

If you have multiple vehicle folders like this:

```
Car1/
    data/
        carcols.meta
        handling.meta
        vehicles.meta
    stream/
        car1.yft
        car1.ytd
        car1_hi.yft

Car2/
    data/
        carcols.meta
        handling.meta
        vehicles.meta
    stream/
        car2.yft
        car2.ytd
        car2_hi.yft
```

This script will convert it into a neat structure:

```
Carpack/
    stream/
        Car1/
            car1.yft
            car1.ytd
            car1_hi.yft
        Car2/
            car2.yft
            car2.ytd
            car2_hi.yft
    data/
        Car1/
            carcols.meta
            handling.meta
            vehicles.meta
        Car2/
            carcols.meta
            handling.meta
            vehicles.meta
```

## ✅ Features

- Fully automated organization
- Supports any number of vehicles
- Keeps `data` and `stream` files properly grouped
- Prevents overwriting with isolated subfolders per vehicle


# [![Example](path/to/thumbnail.png)](https://jumpshare.com/embed/y7c6nl61AyRwp7sDnjrQ)



## 🚀 How to Use

### 1. Requirements

- [Python 3.x](https://www.python.org/downloads/)

### 2. Setup

Clone this repository:

```bash
git clone https://github.com/yourusername/fivem-carpack-organizer.git
cd fivem-carpack-organizer
```

run the `install_packages.bat`

### 3. Configure

Put all of your vehicle folders into the `Car Files` folder

**Example:**
```
HavocCarPacker/
  Car Files/
    audiR8/
    bmwM5/
    golfGTI/

```


### 4. Run the Script

Run the `run_app.bat` file

After running, check the new `[OUTPUT]/` directory for your neatly organized files.

## 📄 License

This project is licensed under the MIT License.
