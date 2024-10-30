#!/usr/bin/env bash

set -e # exit on any error

tmp_dir=$PWD/tmp
export ISEARCHD_SOCKET=$PWD/tmp/isearchd.sock
export ISEARCHD_DB=$PWD/tmp/db.sqlite3
export ISEARCHD_IMAGES_DIR=$PWD/tmp/images
mkdir -p $ISEARCHD_IMAGES_DIR

chmod -R 777 $tmp_dir

isearchd_pid=''

function cleanup {
  echo "Cleanup..."
  rm  -r $tmp_dir
  if [[ -n "$isearchd_pid" ]]
  then
    echo "killing isearchd"
    kill $isearchd_pid
  fi
}

trap cleanup EXIT

echo "Building and starting isearchd..."

export ISEARCH_TEST=1
cd isearchd
python3 -m venv $tmp_dir/isearchd_venv
source $tmp_dir/isearchd_venv/bin/activate
pip install -q -q -r test.requirements.txt
python3 main.py &
isearchd_pid=$!
sleep 2
cd ..

echo "Creating test images"
cp tests/fixtures/test_image.png $ISEARCHD_IMAGES_DIR/1.png
cp tests/fixtures/test_image.png $ISEARCHD_IMAGES_DIR/2.png
cp tests/fixtures/test_image.png $ISEARCHD_IMAGES_DIR/3.png
sleep 1
rm $ISEARCHD_IMAGES_DIR/1.png
mkdir $ISEARCHD_IMAGES_DIR/subdir
cp tests/fixtures/test_image.png $ISEARCHD_IMAGES_DIR/subdir/subfile.png

# create another test dir
mkdir $tmp_dir/another_dir
cp tests/fixtures/test_image.png $tmp_dir/another_dir/img.png

echo "Running reindex with isearchctl for another test dir"
cd isearchctl
python3 -m venv $tmp_dir/ctl_venv
source $tmp_dir/ctl_venv/bin/activate
pip install -q -q -r requirements.txt
python3 main.py reindex $tmp_dir/another_dir
cd ..

echo "Starting and stopping isearchd to check db persistence"
kill $isearchd_pid
cd isearchd
python3 -m venv $tmp_dir/isearchd_venv
source $tmp_dir/isearchd_venv/bin/activate
python3 main.py &
isearchd_pid=$!
sleep 2
cd ..

echo "Building isearchcli"
cd isearchcli
python3 -m venv $tmp_dir/cli_venv
source $tmp_dir/cli_venv/bin/activate
pip install -q -q -r requirements.txt

echo "Running isearchcli"
python3 main.py 'some test query' | sort > /tmp/isearch_test_result.txt
find $tmp_dir -name '*.png' | sort > $tmp_dir/expected_output.txt

set +e
difference=`diff $tmp_dir/expected_output.txt /tmp/isearch_test_result.txt`

if [[ -n $difference  ]]
  then
    echo "Got incorrect output:"
    echo $difference
    echo "Test failed!"
    exit 1
fi

echo "Test passed!"