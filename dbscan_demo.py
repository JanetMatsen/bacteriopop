from dbscan import dbscan
from load_data import load_data
from bacteriopop_utils import extract_features


def dbscan_demo():
    print 'starting up'
    df = load_data()
    print 'load done'
    df = extract_features(df)
    print 'features done'
    dbscan(df, 0.2, 10)

# Run the following code if the file is run at the command line


def main():
    return dbscan_demo()

if __name__ == "__main__":
    main()