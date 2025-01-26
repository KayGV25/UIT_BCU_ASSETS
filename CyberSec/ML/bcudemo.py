import json,os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import optuna  # For hyperparameter tuning
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import ReduceLROnPlateau
from tqdm import tqdm
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
from torch.cuda.amp import GradScaler, autocast
import torch.nn.functional as F
from sklearn.mixture import GaussianMixture
from scipy.signal import find_peaks
import psutil
from sklearn.preprocessing import StandardScaler

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Plots
# Function to compute accuracy per label (class)
def compute_label_accuracy(y_true, y_pred, num_classes):
    cm = confusion_matrix(y_true, y_pred, labels=range(num_classes))
    label_accuracy = cm.diagonal() / cm.sum(axis=1)  # Class-wise accuracy
    return label_accuracy, cm

# Function to plot accuracy for all labels (classes)
def plot_all_label_accuracy(label_accuracy, epoch, output_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(label_accuracy)), label_accuracy)
    plt.title(f"Per-Label Accuracy - Epoch {epoch + 1}")
    plt.xlabel("Label")
    plt.ylabel("Accuracy")
    plt.xticks(range(len(label_accuracy)))
    plt.ylim(0, 1)
    plt.grid()
    plt.savefig(os.path.join(output_dir, f"label_accuracy_epoch_{epoch + 1}.png"))
    plt.close()

# Function to plot accuracy for all labels (classes)
def plot_label_accuracy(label_accuracy, epoch, output_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(label_accuracy)), label_accuracy)
    plt.title(f"Per-Label Accuracy - Epoch {epoch + 1}")
    plt.xlabel("Label")
    plt.ylabel("Accuracy")
    plt.xticks(range(len(label_accuracy)))
    plt.ylim(0, 1)
    plt.grid()
    plt.savefig(os.path.join(output_dir, f"label_accuracy_epoch_{epoch + 1}.png"))
    plt.close()

# Function to plot and save confusion matrix
def plot_confusion_matrix(y_true, y_pred, epoch, output_dir):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=True, yticklabels=True)
    plt.title(f"Confusion Matrix - Epoch {epoch + 1}")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.savefig(os.path.join(output_dir, f"confusion_matrix_epoch_{epoch + 1}.png"))
    plt.close()

# Function to plot accuracy
def plot_accuracy(train_acc, test_acc, output_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(train_acc, label='Train Accuracy', color='blue')
    plt.plot(test_acc, label='Test Accuracy', color='red')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title("Train vs Test Accuracy")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, "accuracy_plot.png"))
    plt.close()

def approximate_with_normal_distribution(column_data, means, stds, k=2, decimal_places=4):
    approximated_values = []
    epsilon = 1e-9  # Small constant to prevent division by zero
    
    for val in column_data:
        # Find nearest mean and std
        nearest_index = np.argmin(abs(val - means))
        nearest_mean = means[nearest_index]
        nearest_std = max(stds[nearest_index], epsilon)

        # Compute dynamic alpha with epsilon adjustment
        distance = abs(val - nearest_mean)

        alpha = min(1, distance / (k * nearest_std))

        # Shift the value
        shift_magnitude = alpha * nearest_std
        shifted_value = val + shift_magnitude * np.sign(nearest_mean - val)

        # Round result
        approximated_values.append(round(shifted_value, decimal_places))
    
    return np.array(approximated_values)

# CustomScale
def shift_outliers_ordered(series, lower_bound, upper_bound):
    # Separate the in-bound and outlier values
    in_bounds = series[(series >= lower_bound) & (series <= upper_bound)]
    below_lower = series[series < lower_bound]
    above_upper = series[series > upper_bound]

    # Map outliers while keeping their relative order
    below_mapped = {val: lower_bound - i for i, val in enumerate(sorted(below_lower, reverse=True), start=1)}
    above_mapped = {val: upper_bound + i for i, val in enumerate(sorted(above_upper), start=1)}

    # Apply mapping
    def map_value(x):
        if x in below_mapped:
            return below_mapped[x]
        elif x in above_mapped:
            return above_mapped[x]
        else:
            return x  # Keep in-bound values unchanged

    return series.map(map_value)

class SRMMCustomScaler:
    def __init__(self, lower_bound=0, upper_bound=29999, shirk=0.1, verbose=False, params_file="scaling_parameters.json"):
        """
        Initialize the scaler with thresholds and parameters.
        """
        self.lower_bound = config.get('lower_bound')
        self.upper_bound = config.get('upper_bound')
        self.verbose = verbose
        self.params_file = params_file
        self.scale_dict = {}
        self.columns = None

        # Check if the parameter file exists and load it if it does
        if os.path.exists(self.params_file):
            self.load_scale_dict(self.params_file)
            if self.verbose:
                print(f"Loaded scaling parameters from {self.params_file}.")

    @staticmethod
    def shrink_outliers(series, lower_bound, upper_bound):
        """Shrink outliers toward the boundary values proportionally."""
        ushirk= config.get('ushirk')
        lshirk= config.get('lshirk')
        ushirk
        def shrink_below(val):
            return lower_bound + (val - lower_bound) * lshirk

        def shrink_above(val):
            return upper_bound - (upper_bound - val) * ushirk

        # Apply shrinking
        series = series.copy()
        series[series < lower_bound] = series[series < lower_bound].apply(shrink_below)
        series[series > upper_bound] = series[series > upper_bound].apply(shrink_above)

        return series

    def save_scale_dict(self, file_path):
        def convert_to_serializable(obj):
            """Recursively convert NumPy types to Python native types."""
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(v) for v in obj]
            return obj  # Return as-is if it's already serializable

        # Convert scale_dict to a serializable format
        serializable_dict = convert_to_serializable(self.scale_dict)

        if os.path.exists(file_path):
            os.remove(file_path)
            if self.verbose:
                print(f"Existing file {file_path} removed.")

        with open(file_path, 'w') as f:
            json.dump(serializable_dict, f, indent=16)

        if self.verbose:
            print(f"Saved scaling parameters to {file_path}.")

    def load_scale_dict(self, file_path):
        """Load scaling parameters from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                self.scale_dict = json.load(f)
            if self.verbose:
                print(f"Loaded scaling parameters from {file_path}.")
        except FileNotFoundError:
            if self.verbose:
                print(f"File {file_path} not found. Scale dictionary will remain empty.")
            self.scale_dict = {}
        except json.JSONDecodeError as e:
            if self.verbose:
                print(f"Error decoding JSON from {file_path}: {e}")
            self.scale_dict = {}

    def fit(self, data):
        """
        Fit the scaler to the data and compute the necessary scaling parameters.
        """
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        self.columns = data.columns

        # Handle outliers and fit Min-Max scaling
        shifted_data = data.copy()
        for col in self.columns:
            shifted_data[col] = self.shrink_outliers(data[col], self.lower_bound, self.upper_bound)

            # Store modified min and max values for columns with adjusted outliers
            modified_min = shifted_data[col].min()
            modified_max = shifted_data[col].max()

            self.scale_dict[col] = {
                "method": "shrink_outliers",
                "original_min": data[col].min(),
                "original_max": data[col].max(),
                "adjusted_min": modified_min,
                "adjusted_max": modified_max,
                "lower_bound": self.lower_bound,
                "upper_bound": self.upper_bound
            }

        if self.verbose:
            print(f"Fitted scaler. Columns: {list(self.columns)}")

        # Save parameters to file
        self.save_scale_dict(self.params_file)

    def transform(self, data):
        """
        Transform the data using the fitted scaler and scale it to [lower_bound, upper_bound].
        """
        if not self.scale_dict:
            raise ValueError("Scaler has not been fitted. Call 'fit' before 'transform'.")

        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data, columns=self.columns)

        shifted_data = data.copy()
        for col in self.columns:
            shifted_data[col] = self.shrink_outliers(data[col], self.lower_bound, self.upper_bound)

        transformed_data = pd.DataFrame(index=shifted_data.index, columns=shifted_data.columns)

        for col in self.columns:
            params = self.scale_dict[col]
            adjusted_min = params["adjusted_min"]
            adjusted_max = params["adjusted_max"]
            lower_bound, upper_bound = params["lower_bound"], params["upper_bound"]

            # Handle columns with no variation
            if adjusted_max == adjusted_min:
                if self.verbose:
                    print(f"Column '{col}' has a constant value. Scaling skipped.")
                transformed_data[col] = shifted_data[col]
            else:
                # Scale data to [lower_bound, upper_bound]
                transformed_data[col] = lower_bound + (
                    (shifted_data[col] - adjusted_min) /
                    (adjusted_max - adjusted_min) * (upper_bound - lower_bound)
                )

            # Debug information
            if self.verbose:
                print(f"Column '{col}':\n"
                      f"Min value after scaling: {transformed_data[col].min()},\n"
                      f"Max value after scaling: {transformed_data[col].max()},\n"
                      f"Adjusted Min: {adjusted_min},\n"
                      f"Adjusted Max: {adjusted_max}.")

        if self.verbose:
            print("Transformed data using the fitted scaler.")

        return transformed_data

    def fit_transform(self, data):
        """
        Fit the scaler to the data and transform it.
        """
        self.fit(data)
        return self.transform(data)

class DSRMMCustomScaler:
    def __init__(self, lower_bound=0, upper_bound=29999, shirk=0.1, verbose=False, params_file="scaling_parameters.json"):
        """
        Initialize the scaler with thresholds and parameters.
        """
        self.lower_bound = config.get('lower_bound')
        self.upper_bound = config.get('upper_bound')
        self.verbose = verbose
        self.params_file = params_file
        self.scale_dict = {}
        self.columns = None

        # Check if the parameter file exists and load it if it does
        if os.path.exists(self.params_file):
            self.load_scale_dict(self.params_file)
            if self.verbose:
                print(f"Loaded scaling parameters from {self.params_file}.")

    @staticmethod
    def shrink_outliers(series, lower_bound, upper_bound):
        """Shrink outliers toward the boundary values proportionally."""
        ushirk= config.get('ushirk')
        lshirk= config.get('lshirk')
        ushirk
        def shrink_below(val):
            return lower_bound + (val - lower_bound) * lshirk

        def shrink_above(val):
            return upper_bound - (upper_bound - val) * ushirk

        # Apply shrinking
        series = series.copy()
        series[series < lower_bound] = series[series < lower_bound].apply(shrink_below)
        series[series > upper_bound] = series[series > upper_bound].apply(shrink_above)

        return series

    def save_scale_dict(self, file_path):
        def convert_to_serializable(obj):
            """Recursively convert NumPy types to Python native types."""
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(v) for v in obj]
            return obj  # Return as-is if it's already serializable

        # Convert scale_dict to a serializable format
        serializable_dict = convert_to_serializable(self.scale_dict)

        if os.path.exists(file_path):
            os.remove(file_path)
            if self.verbose:
                print(f"Existing file {file_path} removed.")

        with open(file_path, 'w') as f:
            json.dump(serializable_dict, f, indent=16)

        if self.verbose:
            print(f"Saved scaling parameters to {file_path}.")

    def load_scale_dict(self, file_path):
        """Load scaling parameters from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                self.scale_dict = json.load(f)
            if self.verbose:
                print(f"Loaded scaling parameters from {file_path}.")
        except FileNotFoundError:
            if self.verbose:
                print(f"File {file_path} not found. Scale dictionary will remain empty.")
            self.scale_dict = {}
        except json.JSONDecodeError as e:
            if self.verbose:
                print(f"Error decoding JSON from {file_path}: {e}")
            self.scale_dict = {}

    def fit(self, data):
        """
        Fit the scaler to the data and compute the necessary scaling parameters.
        """
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        self.columns = data.columns

        # Handle outliers and fit Min-Max scaling
        shifted_data = data.copy()
        for col in self.columns:
            shifted_data[col] = self.shrink_outliers(data[col], self.lower_bound, self.upper_bound)

            # Store modified min and max values for columns with adjusted outliers
            modified_min = shifted_data[col].min()
            modified_max = shifted_data[col].max()

            # Calculate k-neighbor
            threshold=config.get('threshold')
            k_neighbor = min(modified_max / ((self.upper_bound - self.lower_bound) / threshold), 15)

            self.scale_dict[col] = {
                "method": "shrink_outliers",
                "original_min": data[col].min(),
                "original_max": data[col].max(),
                "adjusted_min": modified_min,
                "adjusted_max": modified_max,
                "lower_bound": self.lower_bound,
                "upper_bound": self.upper_bound,
                "k_neighbor": k_neighbor  # Save k-neighbor for downstream use
            }
        if self.verbose:
            print(f"Fitted scaler. Columns: {list(self.columns)}")

        # Save parameters to file
        self.save_scale_dict(self.params_file)

    def transform(self, data):
        """
        Transform the data using the fitted scaler and scale it to [lower_bound, upper_bound].
        """
        if not self.scale_dict:
            raise ValueError("Scaler has not been fitted. Call 'fit' before 'transform'.")

        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data, columns=self.columns)

        shifted_data = data.copy()
        for col in self.columns:
            shifted_data[col] = self.shrink_outliers(data[col], self.lower_bound, self.upper_bound)

        transformed_data = pd.DataFrame(index=shifted_data.index, columns=shifted_data.columns)

        for col in self.columns:
            params = self.scale_dict[col]
            adjusted_min = params["adjusted_min"]
            adjusted_max = params["adjusted_max"]
            lower_bound, upper_bound = params["lower_bound"], params["upper_bound"]

            # Handle columns with no variation
            if adjusted_max == adjusted_min:
                if self.verbose:
                    print(f"Column '{col}' has a constant value. Scaling skipped.")
                transformed_data[col] = shifted_data[col]
            else:
                # Scale data to [lower_bound, upper_bound]
                transformed_data[col] = lower_bound + (
                    (shifted_data[col] - adjusted_min) /
                    (adjusted_max - adjusted_min) * (upper_bound - lower_bound)
                )

            # Debug information
            if self.verbose:
                print(f"Column '{col}':\n"
                      f"Min value after scaling: {transformed_data[col].min()},\n"
                      f"Max value after scaling: {transformed_data[col].max()},\n"
                      f"Adjusted Min: {adjusted_min},\n"
                      f"Adjusted Max: {adjusted_max}.")

        if self.verbose:
            print("Transformed data using the fitted scaler.")

        return transformed_data

    def fit_transform(self, data):
        """
        Fit the scaler to the data and transform it.
        """
        self.fit(data)
        return self.transform(data)

# Configuration Dictionary
Embedingconfig = {
    'scalej': 10,
    'powj': 0.3,
    'stdj': 30.0,
}
config = {
    'threshold': 5,
    'ushirk':0.001,
    'lshirk':0.7,
    'run_optimization':True,
    'save_lrs':True,
    'mxlr': 0.00099,
    'baselr': 0.00004,
    'value_embedding_dim': 64,
    'position_embedding_dim': 12,
    'vocab_size': 150100, # Embedding matrix size
    'lower_bound':100, 
    'upper_bound':149999,
    'batch_size': 256,
    'num_epochs': 30,
    'hidden_size':256, #sequent_dim + embedding_dim + embedding_dim
    'num_layers': 2,
    'dropout': 0.3,
    'num_attention_heads': 4,
    'attention_probs_dropout_prob': 0.1,
    'kernel_size': 3,
    'amplify_embedding_dim': 64,
    'num_graph_layers': 3,
    'nearest_neighbour': 11
}

# Label Mapping
LABEL_MAPPING = {
    'Uploading_Attack': 0,
    'Recon-PingSweep': 1,
    'Backdoor_Malware': 2,
    'XSS': 3,
    'SqlInjection': 4,
    'CommandInjection': 5,
    'BrowserHijacking': 6,
    'DictionaryBruteForce': 7,
    'DDoS-SlowLoris': 8,
    'DDoS-HTTP_Flood': 9,
    'VulnerabilityScan': 10,
    'DoS-HTTP_Flood': 11,
    'Recon-PortScan': 12,
    'Recon-OSScan': 13,
    'Recon-HostDiscovery': 14,
    'DNS_Spoofing': 15,
    'DDoS-ACK_Fragmentation': 16,
    'DDoS-UDP_Fragmentation': 17,
    'MITM-ArpSpoofing': 18,
    'DDoS-ICMP_Fragmentation': 19,
    'Mirai-greip_flood': 20,
    'Mirai-udpplain': 21,
    'Mirai-greeth_flood': 22,
    'BenignTraffic': 23,
    'DoS-SYN_Flood': 24,
    'DoS-TCP_Flood': 25,
    'DoS-UDP_Flood': 26,
    'DDoS-SynonymousIP_Flood': 27,
    'DDoS-RSTFINFlood': 28,
    'DDoS-SYN_Flood': 29,
    'DDoS-PSHACK_Flood': 30,
    'DDoS-TCP_Flood': 31,
    'DDoS-UDP_Flood': 32,
    'DDoS-ICMP_Flood': 33
}
# Load Dataset
input_csv = r"./estimate_1/subset_1.csv"
data = pd.read_csv(input_csv)
features = data.drop('label', axis=1)
headers = features.columns
labels = data['label'].map(LABEL_MAPPING)

config['sequence_length'] = features.shape[1]

config['embedding_dim'] = config['value_embedding_dim'] + config['position_embedding_dim'] + config['amplify_embedding_dim']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    features.values, labels.values, test_size=0.2, random_state=40
)

# Initialize scaler
scaler = DSRMMCustomScaler(verbose=True)

# Fit scaler on X_train
scaler.fit(X_train)
#scaler.fit_quantization(X_train)

# Save scaling parameters
scaler.save_scale_dict("scaling_parameters.json")

#Transform X_train and X_test
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# If X_train_scaled and X_test_scaled are pandas DataFrames, convert them to NumPy arrays
if isinstance(X_train_scaled, pd.DataFrame):
    X_train_scaled = X_train_scaled.to_numpy()
if isinstance(X_test_scaled, pd.DataFrame):
    X_test_scaled = X_test_scaled.to_numpy()

# 2. Save the scaled data to disk
np.save("X_train_scaled.npy", X_train_scaled)
np.save("X_test_scaled.npy", X_test_scaled)

print("Saved X_train_scaled and X_test_scaled to disk.")

# 3. Load the saved data from disk
X_train_loaded = np.load("X_train_scaled.npy")
X_test_loaded = np.load("X_test_scaled.npy")

print("Loaded X_train_scaled from disk. Shape:", X_train_loaded.shape)
print("Loaded X_test_scaled from disk. Shape:", X_test_loaded.shape)

# Continue with tensor conversion after confirming the load process works
train_dataset = TensorDataset(
    torch.tensor(X_train_loaded, dtype=torch.long),  # Convert to long for labels
    torch.tensor(y_train, dtype=torch.long)  # Labels as long (int64)
)
test_dataset = TensorDataset(
    torch.tensor(X_test_loaded, dtype=torch.long),  # Convert to long for labels
    torch.tensor(y_test, dtype=torch.long)  # Labels as long (int64)
)

# Prepare DataLoader
train_loader = DataLoader(train_dataset, batch_size=config['batch_size'], shuffle=True, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=config['batch_size'], shuffle=False, pin_memory=True)

class GraphAvgColAmplifiedEmbedding(nn.Module):
    def __init__(
        self,
        vocab_size,
        value_embedding_dim,
        sequence_length,
        position_embedding_dim,
        amplify_embedding_dim,
        k=config.get('nearest_neighbour'),  # Number of nearest rows
        num_graph_layers=config.get('num_graph_layers'),
        dropout_prob=0.3,
    ):
        super(GraphAvgColAmplifiedEmbedding, self).__init__()

        self.k = k  # Number of nearest embeddings
        self.vocab_size = vocab_size
        self.sequence_length = sequence_length

        # Combined feature dimension (d_v + d_p)
        self.input_feature_dim = value_embedding_dim + position_embedding_dim

        # Value and position embeddings
        self.value_embedding = nn.Embedding(vocab_size, value_embedding_dim)  # E_v
        self.position_embedding = nn.Embedding(sequence_length, position_embedding_dim)  # E_p

        # Graph-based amplification embeddings
        self.graph_layers = nn.ModuleList([
            nn.Linear(
                self.input_feature_dim if i == 0 else amplify_embedding_dim,
                amplify_embedding_dim
            )
            for i in range(num_graph_layers)
        ])

        # Adjacency matrix: Trainable weights for sequence relationships
        self.adjacency_weights = nn.Parameter(
            torch.rand(sequence_length, sequence_length)
        )  # [sequence_length, sequence_length]

        # Dropout for regularization
        self.dropout = nn.Dropout(dropout_prob)

        # Initialize embeddings and adjacency weights
        nn.init.xavier_uniform_(self.adjacency_weights)
        nn.init.xavier_uniform_(self.position_embedding.weight)
        nn.init.xavier_uniform_(self.value_embedding.weight)

    def forward(self, discrete_indices):
        batch_size, seq_len = discrete_indices.size()

        # Step 1: Map input indices to column-constrained neighbors
        rounded_indices = discrete_indices.round()  # Round to integer
        nearest_offsets = torch.arange(
            -self.k // 2, self.k // 2 + 1, device=discrete_indices.device
        ).unsqueeze(0)  # [1, k]

        # Constrain neighbor indices within columns (same sequence index)
        nearest_indices = nearest_offsets + rounded_indices.unsqueeze(-1)  # [batch_size, seq_len, k]
        nearest_indices = nearest_indices.clamp(0, self.vocab_size - 1)  # Clip to valid range

        # Step 2: Gather column-constrained embeddings and compute the average
        # Only gather embeddings for the same sequence position (column constraint)
        nearest_embeddings = self.value_embedding(nearest_indices)  # [batch_size, seq_len, k, value_embedding_dim]
        value_embeddings = nearest_embeddings.mean(dim=-2)  # Average pooling within column neighbors

        # Step 3: Compute position embeddings
        position_ids = torch.arange(seq_len, device=discrete_indices.device).unsqueeze(0).repeat(batch_size, 1)
        position_embeddings = self.position_embedding(position_ids)  # [batch_size, seq_len, position_embedding_dim]

        # Combine value and position embeddings as node features
        node_features = torch.cat((value_embeddings, position_embeddings), dim=-1)  # [batch_size, seq_len, d_v + d_p]

        # Step 4: Amplify embeddings using graph layers
        amplified_embeddings = node_features  # Initialize with F_0
        adjacency_matrix = F.softmax(self.adjacency_weights, dim=-1)  # Normalize adjacency matrix
        adjacency_matrix = adjacency_matrix.unsqueeze(0).expand(batch_size, -1, -1)  # [batch_size, seq_len, seq_len]

        for i, layer in enumerate(self.graph_layers):
            # Propagate embeddings with adjacency matrix
            amplified_embeddings = torch.bmm(adjacency_matrix, amplified_embeddings)  # [batch_size, seq_len, d_v + d_p or amplify_embedding_dim]

            # Ensure the graph layer expects the correct input dimension
            expected_input_dim = layer.in_features
            assert amplified_embeddings.size(-1) == expected_input_dim, (
                f"Mismatch in dimensions: expected {expected_input_dim}, got {amplified_embeddings.size(-1)}"
            )

            # Apply the graph layer
            amplified_embeddings = layer(amplified_embeddings)

            # Apply activation function
            amplified_embeddings = F.relu(amplified_embeddings)

            # Apply dropout for regularization
            amplified_embeddings = self.dropout(amplified_embeddings)

        # Step 5: Concatenate all embeddings
        final_embeddings = torch.cat(
            (value_embeddings, position_embeddings, amplified_embeddings), dim=-1
        )
        # Final dimension: [batch_size, seq_len, value_embedding_dim + position_embedding_dim + amplify_embedding_dim]
        return final_embeddings

def max_norm_landmark_sampling(Q, m):
    """
    Select landmarks based on token norms.

    Args:
        Q (torch.Tensor): Query matrix of shape (batch_size, seq_len, d_k).
        m (int): Number of landmark points to select.

    Returns:
        Q_landmarks (torch.Tensor): Landmark queries of shape (batch_size, m, d_k).
        indices (torch.Tensor): Indices of selected landmarks.
    """
    norms = torch.norm(Q, dim=-1)  # Compute token norms
    _, indices = torch.topk(norms, m, dim=1)  # Select top-m tokens based on norm
    Q_landmarks = torch.gather(Q, 1, indices.unsqueeze(-1).expand(-1, -1, Q.size(-1)))
    return Q_landmarks, indices

def random_landmark_sampling(Q, m):
    """
    Randomly select landmarks from the input tensor.

    Args:
        Q (torch.Tensor): Query matrix of shape (batch_size, seq_len, d_k).
        m (int): Number of landmark points to select.

    Returns:
        Q_landmarks (torch.Tensor): Landmark queries of shape (batch_size, min(m, seq_len), d_k).
        indices (torch.Tensor): Indices of selected landmarks.
    """
    batch_size, seq_len, d_k = Q.size()
    m = min(m, seq_len)  # Ensure m does not exceed seq_len

    # Randomly sample indices without replacement
    indices = torch.randint(0, seq_len, (batch_size, m), device=Q.device)
    Q_landmarks = torch.gather(Q, 1, indices.unsqueeze(-1).expand(-1, -1, Q.size(-1)))
    return Q_landmarks, indices

#Anomaly Aware SelfAttention

class AnomalyAwareSelfAttention(nn.Module):
    def __init__(self, config):
        super(AnomalyAwareSelfAttention, self).__init__()

        # Extract the required parameters from the config dictionary
        self.hidden_size = config['hidden_size']
        self.attention_probs_dropout_prob = config['attention_probs_dropout_prob']

        # Define query and value layers with dimension `hidden_size`
        self.query = nn.Linear(self.hidden_size, self.hidden_size)
        self.value = nn.Linear(self.hidden_size, self.hidden_size)

        # Dropout layer for attention probabilities
        self.dropout = nn.Dropout(self.attention_probs_dropout_prob)

        # Anomaly matrix for calculating anomaly scores within the single vector space
        self.anomaly_matrix = nn.Parameter(torch.zeros(self.hidden_size, self.hidden_size))
        self.threshold = nn.Parameter(torch.tensor(1.0))

        # Initialize weights
        self.init_weights()

    def init_weights(self):
        """
        Custom initialization for weights to incorporate input sensitivity.
        """
        # Initialize query and value weights
        gain = 1.2 # 1.0 for gelu
        nn.init.xavier_uniform_(self.query.weight, gain=gain)
        nn.init.xavier_uniform_(self.value.weight, gain=gain)
        nn.init.zeros_(self.query.bias)
        nn.init.zeros_(self.value.bias)
        # Initialize anomaly matrix with small random values for stability
        nn.init.uniform_(self.anomaly_matrix, a=-2.0, b=2.0)

    def forward(self, hidden_states, attention_mask=None):
        """
        Forward pass for anomaly-aware self-attention, capturing magnitude sensitivity.
        """
        batch_size, seq_len, input_dim = hidden_states.size()

        # Ensure that hidden_states matches the expected input dimension for this layer
        if input_dim != self.hidden_size:
            raise ValueError(f"Expected hidden_states with last dimension {self.hidden_size}, but got {input_dim}.")

        # Compute the norm (magnitude) of the input vectors
        input_norm = torch.norm(hidden_states, dim=-1, keepdim=True)  # Shape: [batch_size, seq_len, 1]

        # Scale the hidden states by their magnitude
        scaled_hidden_states = hidden_states / (input_norm + 1e-9)  # Prevent division by zero

        # Generate query and value projections (magnitude-sensitive)
        query_layer = self.query(scaled_hidden_states)  # Shape: [batch_size, seq_len, hidden_size]
        value_layer = self.value(scaled_hidden_states)  # Shape: [batch_size, seq_len, hidden_size]

        # Anomaly transformation: apply anomaly matrix to query_layer
        transformed_query = torch.matmul(query_layer, self.anomaly_matrix)  # Shape: [batch_size, seq_len, hidden_size]

        # Compute magnitude-sensitive attention scores
        anomaly_scores = torch.matmul(query_layer, transformed_query.transpose(-1, -2)) / math.sqrt(self.hidden_size)
        # Shape of anomaly_scores: [batch_size, seq_len, seq_len]

        # Apply attention mask if provided
        if attention_mask is not None:
            attention_mask = attention_mask.unsqueeze(1)  # Shape [batch_size, 1, seq_len]
            anomaly_scores = anomaly_scores + attention_mask

        # Softmax to obtain attention probabilities
        attention_probs = nn.Softmax(dim=-1)(anomaly_scores)
        attention_probs = self.dropout(attention_probs)
        
        # Compute context layer as weighted sum of value_layer based on attention_probs
        context_layer = torch.matmul(attention_probs, value_layer)  # Shape: [batch_size, seq_len, hidden_size]

        # Rescale context by input magnitude (restore magnitude sensitivity)
        context_layer = context_layer * input_norm

        return context_layer

class StackedSelfAttention(nn.Module):
    def __init__(self, attention_layers):
        super(StackedSelfAttention, self).__init__()
        
        # `attention_layers` is expected to be a list of lists, where each inner list
        # represents a collection of parallel attention modules for that layer.
        self.layers = nn.ModuleList(
            [nn.ModuleList(layer) for layer in attention_layers]
        )

    def forward(self, hidden_states, attention_mask=None):
        for layer in self.layers:
            # For each attention mechanism in the layer, process hidden states in parallel
            attention_outputs = [attention(hidden_states, attention_mask) for attention in layer]
            
            # Aggregate the outputs of all attention mechanisms (e.g., by averaging or concatenating)
            # Here we use concatenation as an example.
            hidden_states = torch.cat(attention_outputs, dim=-1)
        
        return hidden_states

class DetectionModelLSTM(nn.Module):
    def __init__(self, config):
        super(DetectionModelLSTM, self).__init__()

        # Embedding layer
        self.embedding = GraphAvgColAmplifiedEmbedding(
            vocab_size=config['vocab_size'],
            value_embedding_dim=config['value_embedding_dim'],
            sequence_length=config['sequence_length'],
            position_embedding_dim=config['position_embedding_dim'],
            amplify_embedding_dim=config['amplify_embedding_dim'],
            num_graph_layers=config.get('num_graph_layers', 3),
            dropout_prob=config.get('dropout', 0.3),
            k=config.get('nearest_neighbour', 7)
        )
        self.embedding_activation = nn.GELU()  # Activation applied after embeddings

        # Combined embedding dimension
        combined_embedding_dim = (
            config['value_embedding_dim']
            + config['position_embedding_dim']
            + config['amplify_embedding_dim']
        )

        # LSTM layer
        self.lstm = nn.LSTM(
            input_size=combined_embedding_dim,
            hidden_size=config['hidden_size'],
            num_layers=config.get('num_lstm_layers', 2),
            batch_first=True,
            dropout=config.get('dropout', 0.3),
            bidirectional=True  # Bidirectional LSTM
        )

        # Fully connected layers
        self.fc_hidden = nn.Linear(2 * config['hidden_size'], config['hidden_size'])
        self.fc_activation = nn.GELU()  # Activation after hidden layer
        self.fc_output = nn.Linear(config['hidden_size'], len(LABEL_MAPPING))  # Output layer for classification

    def forward(self, discrete_indices, attention_mask=None):
        # Pass input through embedding layer
        combined_embeddings = self.embedding(discrete_indices)
        combined_embeddings = self.embedding_activation(combined_embeddings)

        # Pass embeddings through LSTM
        lstm_output, _ = self.lstm(combined_embeddings)

        # Use the output from the last time step
        output = lstm_output[:, -1, :]

        # Pass through fully connected layers
        output = self.fc_hidden(output)
        output = self.fc_activation(output)
        output = self.fc_output(output)
        return output
# Optuna Objective Function
num_classes = len(LABEL_MAPPING) 

def objective(trial): 
    """
    Objective function for Optuna to optimize the learning rate.
    """
    # Suggest a learning rate
    baselr= config.get('baselr', 0.000001)
    mxlr= config.get('mxlr', 0.0001)
    learning_rate = trial.suggest_float('lr', baselr, mxlr, log=True)

    # Initialize model, optimizer, and scheduler
    model = DetectionModelLSTM(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    criterion = nn.CrossEntropyLoss()
    Trialscheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3, min_lr=1e-5)

    for epoch in range(1):  # Optuna trial duration
        # Training step
        train_loss, _ = train_epoch(model, train_loader, optimizer, criterion, epoch)

        # Evaluation step
        test_loss, _, _, _, _, _ = evaluate(model, test_loader, criterion, num_classes)

        # Update the `Trialscheduler` with the validation loss
        Trialscheduler.step(test_loss)

        # Report the test loss to Optuna
        trial.report(test_loss, epoch)

        # Prune the trial if it's not promising
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return test_loss  # Minimize validation loss

# Training loop

def train_epoch(model, loader, optimizer, criterion, epoch, scheduler=None):
    model.train()
    total_loss, correct, total = 0, 0, 0
    progress_bar = tqdm(loader, desc=f"Epoch {epoch + 1}", leave=False)

    for batch_X, batch_y in progress_bar:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)

        # Forward pass
        optimizer.zero_grad()
        logits = model(batch_X)
        loss = criterion(logits, batch_y)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Step the scheduler if provided
        if scheduler is not None:
            scheduler.step()

        # Track metrics
        total_loss += loss.item()
        correct += (torch.argmax(logits, dim=1) == batch_y).sum().item()
        total += batch_y.size(0)
        progress_bar.set_postfix(loss=loss.item(), accuracy=100 * correct / total)

    return total_loss / len(loader), 100 * correct / total

# Evaluation function
def evaluate(model, loader, criterion, num_classes):
    """
    Evaluate the model on the given data loader and compute:
    - Total loss
    - Overall accuracy
    - Per-label accuracy
    - Confusion matrix
    """
    model.eval()
    total_loss, correct, total = 0, 0, 0
    all_preds, all_targets = [], []

    with torch.no_grad():
        for batch_X, batch_y in loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)

            # Forward pass
            logits = model(batch_X)

            # Compute loss
            loss = criterion(logits, batch_y)
            total_loss += loss.item()

            # Predictions
            preds = torch.argmax(logits, dim=1)

            # Compute batch-level accuracy
            correct += (preds == batch_y).sum().item()
            total += batch_y.size(0)

            # Collect predictions and targets for label-level accuracy
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(batch_y.cpu().numpy())

    # Compute label-wise accuracy and confusion matrix
    label_accuracy, cm = compute_label_accuracy(all_targets, all_preds, num_classes)

    # Verify consistency of predictions and targets
    assert len(all_preds) == len(all_targets), "Mismatch between predictions and targets!"

    # Overall loss and accuracy
    avg_loss = total_loss / len(loader)
    overall_accuracy = 100 * correct / total

    return avg_loss, overall_accuracy, all_preds, all_targets, label_accuracy, cm

# Custom Learning Rate Scheduler
class CustomLRScheduler:
    def __init__(self, optimizer, lr_list, switch_epochs):
        """
        Args:
        - optimizer: PyTorch optimizer instance.
        - lr_list: List of learning rates (from larger to smaller).
        - switch_epochs: List of epochs at which to switch learning rates.
        """
        self.optimizer = optimizer
        self.lr_list = lr_list
        self.switch_epochs = switch_epochs

    def step(self, epoch):
        """
        Update the learning rate based on the current epoch.
        """
        # Determine the current learning rate based on the epoch
        for i, switch_epoch in enumerate(self.switch_epochs):
            if epoch < switch_epoch:
                lr = self.lr_list[i]
                break
        else:
            lr = self.lr_list[-1]  # Use the smallest learning rate after all switches

        # Apply the learning rate to all parameter groups
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        print(f"Epoch {epoch}: Learning Rate set to {lr}")

# Final Training Function
def final_training():
    """
    Train the model with the best learning rates loaded from lrrate.json and generate evaluation plots.
    """
    # Load learning rates from JSON file
    output_dir = "training_outputs"
    os.makedirs(output_dir, exist_ok=True)
    try:
        with open("lrrate.json", "r") as f:
            lr_data = json.load(f)
            lr_list = sorted(lr_data["top_4_lrs"], reverse=True)  # Sort from largest to smallest
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        raise ValueError("Error loading learning rates from 'lrrate.json': Ensure the file exists and is correctly formatted.") from e

    # Validate learning rate ranges
    baselr= config.get('baselr', 0.000001)
    mxlr= config.get('mxlr', 0.0001)

    assert all(baselr <= lr <= mxlr for lr in lr_list), "One or more learning rates are out of the expected range [1e-5, 1e-3]."

    # Define switch epochs for the custom scheduler
    switch_epochs = [config['num_epochs'] // len(lr_list) * i for i in range(1, len(lr_list))]

    # Initialize model, optimizer, and scheduler for final training
    model = DetectionModelLSTM(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr_list[0], weight_decay=1e-5)
    criterion = nn.CrossEntropyLoss()

    # CyclicLR for intra-epoch dynamics
    scheduler = torch.optim.lr_scheduler.CyclicLR(
        optimizer,
        base_lr=0.9 * lr_list[0],
        max_lr=1.1 * lr_list[0],
        step_size_up=1000,
        mode='triangular',
        cycle_momentum=False
    )

    # Custom scheduler for epoch-level adjustments
    custom_scheduler = CustomLRScheduler(optimizer, lr_list=lr_list, switch_epochs=switch_epochs)
    
    # Directory to save plots and outputs
    output_dir = "training_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Training loop
    train_accuracies, test_accuracies = [], []
    for epoch in range(config['num_epochs']):
        # Update learning rate using CustomLRScheduler
        custom_scheduler.step(epoch)

        # Training step
        train_loss, train_accuracy = train_epoch(
            model, train_loader, optimizer, criterion, epoch, scheduler
        )

        # Evaluation step
        test_loss, test_accuracy, test_preds, test_targets, label_accuracy, cm = evaluate(
            model, test_loader, criterion, num_classes
        )

        # Log metrics
        print(f"Epoch {epoch + 1}:")
        print(f"  Train Loss = {train_loss:.4f}, Train Accuracy = {train_accuracy:.2f}%")
        print(f"  Test Loss = {test_loss:.4f}, Test Accuracy = {test_accuracy:.2f}%")

        train_accuracies.append(train_accuracy)
        test_accuracies.append(test_accuracy)
        # Plot and save confusion matrix
        plot_confusion_matrix(test_targets, test_preds, epoch, output_dir)

        # Plot and save accuracy graph
        plot_accuracy(train_accuracies, test_accuracies, output_dir)

        # Plot and save per-label accuracy
        plot_label_accuracy(label_accuracy, epoch, output_dir)

        # Update learning rate (only if not using CyclicLR as primary)
        # custom_scheduler.step(epoch)
    print("Training Complete. Results and plots saved in:", output_dir)
    return train_accuracies, test_accuracies
run_optimization = config.get('run_optimization', True) 
save_results = config.get('save_lrs', True)

if run_optimization:
    # Run Optuna optimization
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=20)

    if save_results:
        # Save the best 4 learning rates to a JSON file
        good_lrs = [trial.params['lr'] for trial in study.trials if trial.state == optuna.trial.TrialState.COMPLETE]

        # Sort by test loss and select the top 4
        sorted_trials = sorted(study.trials, key=lambda t: t.value if t.state == optuna.trial.TrialState.COMPLETE else float('inf'))
        top_4_lrs = [trial.params['lr'] for trial in sorted_trials[:4]]

        with open("lrrate.json", "w") as f:
            json.dump({"good_lrs": good_lrs, "top_4_lrs": top_4_lrs}, f, indent=4)

        print(f"Top 4 learning rates: {top_4_lrs}")

# Final Training
train_accuracies, test_accuracies = final_training()
