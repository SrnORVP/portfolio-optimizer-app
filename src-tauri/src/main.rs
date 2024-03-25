// #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[allow(dead_code)]
use pyo3::prelude::*;
use pyo3::types::*;

#[allow(unused_imports)]
use std::fmt::format;
use std::fs;
use std::path;
use std::path::Path;

// use tauri::Manager;

// ------------------------------------------------------------------------------------------------------------
// Main

fn main() -> () {
    run_main();
}

// fn main() {
//     let app = tauri::Builder::default().setup(|app| {
//         {
//             let window = app.get_window("main").unwrap();
//             // window.open_devtools();
//             // window.close_devtools();
//         }
//         Ok(())
//     });

//     app.invoke_handler(tauri::generate_handler![
//         server_run_health_metric,
//         server_validate,
//         server_debug
//     ])
//     .run(tauri::generate_context!())
//     .expect("error while running tauri application");
// }

// ------------------------------------------------------------------------------------------------------------
// Tauri

#[allow(dead_code)]
// #[tauri::command(rename_all = "snake_case")]
fn run_main() -> String {
    let entry_script = py_script_main();
    let fn_str = &String::from("none");
    let py_res = pyfunc_runtime(entry_script, "main", (fn_str, fn_str));
    format!("Success with input")
}

// ------------------------------------------------------------------------------------------------------------
// PyO3

#[allow(dead_code)]
fn py_script_main() -> &'static str {
    let py_script = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py-app/main.py"));
    py_script
}

#[allow(dead_code)]
fn py_import_other(py: Python<'_>) {
    let py_script1 = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py-app/weights.py"));
    let _ = PyModule::from_code(py, py_script1, "weights", "weights");

    let py_script2 = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py-app/formulas.py"));
    let _ = PyModule::from_code(py, py_script2, "formulas", "formulas");

    let py_script3 = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py-app/frontier.py"));
    let _ = PyModule::from_code(py, py_script3, "frontier", "frontier");
}

#[allow(dead_code)]
fn py_lib_import(py: Python<'_>) -> PyResult<()> {
    let pypath = Path::new(r#"D:\RustRoot\RustPolars\00_venv\portopt\Lib\site-packages"#);
    let syspath: &PyList = py.import("sys")?.getattr("path")?.downcast()?;
    syspath.insert(0, pypath)
}

#[allow(dead_code)]
#[allow(unused_variables)]
fn pyfunc_runtime(py_script: &str, func_name: &str, func_args: (&String, &String)) -> String {
    // A runtime with apt modules and params for the a function
    // Input: python script
    // name of the python function
    // corresponding function params

    // println!("{:?}{:?}", py_command, py_args);
    let py_res = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
        // Append lib path to python, import search_import
        let _ = py_lib_import(py);
        py_import_other(py);
        // Append lib path to python, import search_import

        let app: Py<PyAny> = PyModule::from_code(py, py_script, "", "")?
            .getattr(func_name)?
            .into();

        // see how to separate the app with the runtime
        // println!("{:?}", app);
        app.call1(py, func_args)
    });

    match py_res {
        Ok(py) => py.to_string(),
        Err(e) => {
            let err_string = e.to_string();
            println!("{}", err_string);
            err_string
        }
    }
}

// ------------------------------------------------------------------------------------------------------------
