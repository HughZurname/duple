import pytest

import dedupe
import pandas as pd
from pandas.util.testing import assert_frame_equal
from io import StringIO
from duple.datautils import data_prep, data_cluster, select_fields, clean_df


@pytest.fixture
def input_frame():
    csv = StringIO(
        """given_name,surname,date_of_birth,sex
le ah,√Ösheim,25/10/1990,f
emalene,ƒåern√ù,16/08/1988,f
emalane,ƒåern√ù,16/08/1988,f
gianni,saga,26/01/2011,f
eliza,smithula,21/05/1988,f
darcy,clausson,03/05/1981,m
shenae,zazi,17/06/1987,f
amber,wackerle,20/02/1992,f
george,loo,18/10/2009,f
jack,scollard,09/04/1977,f
madilda,e instein,06/05/1986,f
leah,ryers,18/04/1993√,f
shenae,zazi,17/06/1987,f
kira,strampher,30/04/1991,f
amber,wack erle,20/02/1992,f
george,loo,18/10/2009,f
jack,scollard,09/04/1977,f
madilda,einstein,06/05/1986,f
lea√h,ryers,18/04/1993,f
mitchell,widj aja,05/04/1996,f"""
    )

    return pd.read_csv(csv)


@pytest.fixture
def expected_frame():
    csv = StringIO(
        """given_name,surname,date_of_birth,sex
leah,osheim,25/10/1990,f
emalene,faernu,16/08/1988,f
emalane,faernu,16/08/1988,f
gianni,saga,26/01/2011,f
eliza,smithula,21/05/1988,f
darcy,clausson,03/05/1981,m
shenae,zazi,17/06/1987,f
amber,wackerle,20/02/1992,f
george,loo,18/10/2009,f
jack,scollard,09/04/1977,f
madilda,einstein,06/05/1986,f
leah,ryers,18/04/1993,f
shenae,zazi,17/06/1987,f
kira,strampher,30/04/1991,f
amber,wackerle,20/02/1992,f
george,loo,18/10/2009,f
jack,scollard,09/04/1977,f
madilda,einstein,06/05/1986,f
leah,ryers,18/04/1993,f
mitchell,widjaja,05/04/1996,f"""
    )

    return pd.read_csv(csv)


@pytest.fixture
def expected_dict(expected_frame):
    return dict(zip(expected_frame.index, expected_frame.to_dict("records")))


@pytest.fixture
def mock_deduper(mocker, monkeypatch):
    mock_deduper = mocker.Mock()
    monkeypatch.setattr(dedupe, "Dedupe", mock_deduper)

    return mock_deduper.return_value


@pytest.fixture
def mock_deduper_match(mocker, mock_deduper):
    mock_match = mocker.Mock(
        return_value=[
            ((7, 14), (0.9999975, 0.9999975)),
            ((9, 16), (0.9999975, 0.9999975)),
            ((10, 17), (0.9999975, 0.9999975)),
        ]
    )
    mock_deduper.match = mock_match
    return mock_match


def test_data_prep(input_frame, expected_frame, expected_dict):
    expected_frame["dictionary"] = expected_frame.to_dict("records")
    prepped_df, prepped_data_d = data_prep(input_frame)

    assert_frame_equal(prepped_df, expected_frame)
    assert prepped_data_d == expected_dict


def test_data_cluster(mock_deduper, mock_deduper_match, input_frame, expected_frame):
    expected_cluster = pd.read_csv(
        StringIO(
            """given_name,surname,date_of_birth,sex,cluster_id,confidence
jack,scollard,09/04/1977,f,1.0,0.9999975
madilda,einstein,06/05/1986,f,2.0,0.9999975
jack,scollard,09/04/1977,f,1.0,0.9999975
madilda,einstein,06/05/1986,f,2.0,0.9999975"""
        )
    )
    clustered, number = data_cluster(mock_deduper, input_frame, 1)
    cluster_results = expected_frame.join(clustered, how="left")
    cluster_results = cluster_results[cluster_results["cluster_id"] > 0]
    assert_frame_equal(
        cluster_results.reset_index(drop=True), expected_cluster.reset_index(drop=True)
    )
    assert number == 3


def test_clean_df(input_frame, expected_frame):
    assert_frame_equal(clean_df(input_frame), expected_frame)


def test_select_fields():
    input_fields = [
        "given_name",
        "surname",
        ["date_of_birth", "DateTime"],
        "sex",
        ["address", "Address"],
    ]
    expected_fields = [
        {"field": "given_name", "type": "String"},
        {"field": "surname", "type": "String"},
        {"field": "date_of_birth", "type": "DateTime"},
        {"field": "sex", "type": "String"},
        {"field": "address", "type": "Address"},
    ]
    assert select_fields(input_fields) == expected_fields
