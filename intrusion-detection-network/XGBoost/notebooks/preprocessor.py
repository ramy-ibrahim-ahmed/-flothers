import pandas as pd


def preprocess(data, scaler, encoder, train):
    features = data.drop(columns=["outcome", "level"])
    labels = data["outcome"]
    levels = data["level"]

    numerical_columns = features.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = features.select_dtypes(include=["object"]).columns.tolist()

    if train:
        scaled = scaler.fit_transform(features[numerical_columns])
        encoded = encoder.fit_transform(features[categorical_columns]).toarray()
        dummy_columns = encoder.get_feature_names_out(categorical_columns)
    else:
        scaled = scaler.transform(features[numerical_columns])
        encoded = encoder.transform(features[categorical_columns]).toarray()
        dummy_columns = encoder.get_feature_names_out(categorical_columns)

    scaled_data = pd.DataFrame(scaled, columns=numerical_columns, index=features.index)

    encoded_data = pd.DataFrame(encoded, columns=dummy_columns, index=features.index)

    features = pd.concat([scaled_data, encoded_data], axis=1)
    labels = labels.apply(lambda x: 0 if x == "normal" else 1)
    return features, labels, levels, encoder


def reduction(data, pca):
    return pca.transform(data)
