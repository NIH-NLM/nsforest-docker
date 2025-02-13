from pathlib import Path
import subprocess
import unittest

import pandas as pd


class TestNSForestContainer(unittest.TestCase):

    def read_lists_and_assert_equal(self):

        # Compare actual and expected results lists
        pd.testing.assert_frame_equal(
            pd.read_csv(self.results_path), pd.read_csv(self.expected_results_path)
        )

        # Compare actual and expected supplementary lists
        pd.testing.assert_frame_equal(
            pd.read_csv(self.supplementary_path),
            pd.read_csv(self.expected_supplementary_path),
            check_exact=False,
            rtol=1e-9,
            atol=1e-3,
        )

    def setUp(self):

        # Assign paths to H5AD files
        self.data_path = "/root/tests/test_data"
        self.adata_path = f"{self.data_path}/adata_layer1.h5ad"
        self.pp_adata_path = f"{self.data_path}/adata_layer1_pp.h5ad"
        self.gd_adata_path = f"{self.data_path}/adata_layer1_gd.h5ad"
        self.gd_cm_adata_path = f"{self.data_path}/adata_layer1_gd_cm.h5ad"
        self.gd_cm_cs_adata_path = f"{self.data_path}/adata_layer1_gd_cm_cs.h5ad"

        # Assign paths to CSV files
        self.results_path = f"{self.data_path}/cluster_results.csv"
        self.expected_results_path = f"{self.data_path}/expected_cluster_results.csv"
        self.supplementary_path = f"{self.data_path}/cluster_supplementary.csv"
        self.expected_supplementary_path = (
            f"{self.data_path}/expected_cluster_supplementary.csv"
        )

        # Assign path to executable
        self.ns_forest_path = "/root/NSForest/nsforest.py"

        # Assign cluster header
        self.cluster_header = "cluster"

    def test_running_nsforest(self):

        # Run NSForest
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--run-nsforest-with-preprocessing",
                "-c",
                self.cluster_header,
                self.adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare actual and expected results and supplementary lists
        self.read_lists_and_assert_equal()

    def test_running_preprocessing_and_nsforest(self):

        # Run preprocessing
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--preprocess-adata-file",
                "-c",
                self.cluster_header,
                self.adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Run NSForest
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--run-nsforest-without-preprocessing",
                "-c",
                self.cluster_header,
                self.pp_adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare actual and expected results and supplementary lists
        self.read_lists_and_assert_equal()

    def test_running_preprocessing_steps_and_nsforest(self):

        # Generate dendrogram
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--generate-scanpy-dendrogram",
                "-c",
                self.cluster_header,
                self.adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Calculate medians
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--calculate-cluster-medians-per-gene",
                "-c",
                self.cluster_header,
                self.gd_adata_path,
            ]
        )

        # Calculate scores
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--calculate-binary-scores-per-gene-per-cluster",
                "-c",
                self.cluster_header,
                self.gd_cm_adata_path,
            ]
        )

        # Run NSForest
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--run-nsforest-without-preprocessing",
                "-c",
                self.cluster_header,
                self.gd_cm_cs_adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare actual and expected results and supplementary lists
        self.read_lists_and_assert_equal()

    def tearDown(self):

        # Clean up
        [file.unlink() for file in Path(self.data_path).glob("adata_layer1_*.h5ad")]
        [
            file.unlink()
            for file in Path(self.data_path).glob(f"{self.cluster_header}_*.csv")
        ]


if __name__ == "__main__":
    unittest.main()
