from gmm import gmm
from load_data import load_data
from bacteriopop_utils import extract_features

def gmm_demo():
    df = load_data()
    df = extract_features(df)
    features_list = list(df.columns.values)[1:]
    gmm(df, features_list)

# Run the following code if the file is run at the command line
def main():
    return gmm_demo()

if __name__ == "__main__":
    main()