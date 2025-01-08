import subprocess
import unittest


class TestNSForestContainer(unittest.TestCase):

    def setUp(self):

        # Assign path to data and output
        self.data_path = "/root/tests/test_data"

        self.adata_path = f"{self.data_path}/adata_layer1.h5ad"

        self.pp_adata_path = f"{self.data_path}/adata_layer1_pp.h5ad"

        self.gd_adata_path = f"{self.data_path}/adata_layer1_gd.h5ad"
        self.gd_cm_adata_path = f"{self.data_path}/adata_layer1_gd_cm.h5ad"
        self.gd_cm_cs_adata_path = f"{self.data_path}/adata_layer1_gd_cm_cs.h5ad"

        self.output_path = f"{self.data_path}/cluster_results.csv"
        self.expected_output_path = f"{self.data_path}/expected_cluster_results.csv"

        # Assign path to executable
        self.ns_forest_path = "/root/NSForest/nsforest.py"

    def test_running_nsforest(self):

        # Run NSForest
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--run-nsforest-with-preprocessing",
                "-c",
                "cluster",
                self.adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare output with expected output
        with open(self.output_path) as output:
            with open(self.expected_output_path) as expected:
                self.assertListEqual(list(output), list(expected))

    def test_running_preprocessing_and_nsforest(self):

        # Run preprocessing
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--preprocess-adata-file",
                "-c",
                "cluster",
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
                "cluster",
                self.pp_adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare output with expected output
        with open(self.output_path) as output:
            with open(self.expected_output_path) as expected:
                self.assertListEqual(list(output), list(expected))

    def test_running_preprocessing_steps_and_nsforest(self):

        # Generate dendrogram
        subprocess.run(
            [
                "python",
                self.ns_forest_path,
                "--generate-scanpy-dendrogram",
                "-c",
                "cluster",
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
                "cluster",
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
                "cluster",
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
                "cluster",
                self.gd_cm_cs_adata_path,
                "-d",
                self.data_path,
            ]
        )

        # Compare output with expected output
        with open(self.output_path) as output:
            with open(self.expected_output_path) as expected:
                self.assertListEqual(list(output), list(expected))


    def tearDown(self):

        # Clean up
        subprocess.run(["rm", self.output_path])
        subprocess.run(["rm", self.pp_adata_path])
        subprocess.run(["rm", self.gd_adata_path])
        subprocess.run(["rm", self.gd_cm_adata_path])
        subprocess.run(["rm", self.gd_cm_cs_adata_path])


if __name__ == "__main__":
    unittest.main()
